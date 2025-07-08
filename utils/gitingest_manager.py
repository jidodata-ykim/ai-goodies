#!/usr/bin/env python3
"""
GitIngest Manager - Manages repository ingestion with exclusions and token counting
"""

import yaml
import subprocess
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import json
import hashlib
import requests
from typing import Dict, List, Optional, Tuple

class GitIngestManager:
    def __init__(self, config_file: str = "gitingest.yaml"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.output_dir = Path(self.config['settings']['output_dir'])
        self.output_dir.mkdir(exist_ok=True)
        
        # Expand token counter path
        self.token_counter = os.path.expandvars(self.config['settings']['token_counter'])
        
    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _save_config(self):
        """Save configuration back to YAML file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
    
    def _get_exclusions(self, repo_name: str, profile: str = "standard") -> List[str]:
        """Get combined exclusions for a repository and profile"""
        repo_config = self.config['repositories'].get(repo_name)
        if not repo_config:
            raise ValueError(f"Repository '{repo_name}' not found in configuration")
        
        exclusions = repo_config.get('exclusions', []).copy()
        
        # Add profile-specific exclusions
        if profile in self.config['profiles']:
            profile_exclusions = self.config['profiles'][profile].get('additional_exclusions', [])
            exclusions.extend(profile_exclusions)
        
        return exclusions
    
    def _build_gitingest_command(self, repo_name: str, output_file: str, profile: str = "standard") -> List[str]:
        """Build gitingest command with exclusions"""
        repo_config = self.config['repositories'][repo_name]
        source = repo_config['source']
        exclusions = self._get_exclusions(repo_name, profile)
        
        cmd = ['gitingest', source, '-o', output_file]
        
        # Add max size if specified
        max_size = self.config['settings'].get('default_max_size')
        if max_size:
            cmd.extend(['-s', str(max_size)])
        
        # Add exclusions
        for exclusion in exclusions:
            cmd.extend(['-e', exclusion])
        
        return cmd
    
    def _count_tokens(self, file_path: str) -> Tuple[int, int]:
        """Count tokens using tc command. Returns (token_count, char_count)"""
        if not Path(self.token_counter).exists():
            print(f"Warning: Token counter not found at {self.token_counter}")
            # Fallback to character count estimation
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                char_count = len(content)
                # Rough estimation: 1 token ≈ 4 characters
                return char_count // 4, char_count
        
        try:
            # Run tc command
            result = subprocess.run(
                [self.token_counter, file_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output (tc outputs "token_count filename")
            output_parts = result.stdout.strip().split()
            if output_parts:
                token_count = int(output_parts[0])
            else:
                raise ValueError("Unable to parse token counter output")
            
            # Get character count
            with open(file_path, 'r', encoding='utf-8') as f:
                char_count = len(f.read())
            
            return token_count, char_count
            
        except subprocess.CalledProcessError as e:
            print(f"Error running token counter: {e}")
            # Fallback
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                char_count = len(content)
                return char_count // 4, char_count
    
    def _get_file_hash(self, file_path: str) -> str:
        """Calculate file hash for versioning"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    
    def _format_token_count(self, count: int) -> str:
        """Format token count in human readable format (e.g., 482k, 1.2M)"""
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1000:
            return f"{count // 1000}k"
        else:
            return str(count)
    
    def _get_github_version(self, repo_path: str) -> Optional[str]:
        """Get the latest release version from GitHub"""
        # Try to get GitHub URL from git remote
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'config', '--get', 'remote.origin.url'],
                capture_output=True,
                text=True,
                check=True
            )
            remote_url = result.stdout.strip()
            
            # Extract owner/repo from URL
            if 'github.com' in remote_url:
                if remote_url.endswith('.git'):
                    remote_url = remote_url[:-4]
                parts = remote_url.split('/')[-2:]
                owner, repo = parts[0], parts[1]
                
                # Get latest release from GitHub API
                api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
                try:
                    response = requests.get(api_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        tag_name = data.get('tag_name', '')
                        # Clean up version (remove 'v' prefix if present)
                        if tag_name.startswith('v'):
                            tag_name = tag_name[1:]
                        return tag_name
                except Exception as e:
                    print(f"Warning: Could not fetch GitHub release: {e}")
                    
        except subprocess.CalledProcessError:
            pass
        
        return None
    
    def ingest(self, repo_name: str, profile: str = "standard", version: Optional[str] = None):
        """Ingest a repository with specified profile"""
        print(f"\n=== Ingesting {repo_name} with profile '{profile}' ===")
        
        # Generate temporary output filename first
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"{repo_name}_temp_{timestamp}.md"
        temp_output_path = self.output_dir / temp_filename
        
        # Build and run gitingest command with temporary file
        cmd = self._build_gitingest_command(repo_name, str(temp_output_path), profile)
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            
            # Count tokens
            print(f"\nCounting tokens...")
            token_count, char_count = self._count_tokens(str(temp_output_path))
            
            # Count files
            with open(temp_output_path, 'r') as f:
                content = f.read()
                file_count = content.count('\n```')  #FIXME_CLAUDE: Rough count of code blocks
            
            # Get version if not provided
            if not version:
                repo_config = self.config['repositories'][repo_name]
                source_path = repo_config['source']
                version = self._get_github_version(source_path)
                if not version:
                    version = "latest"
            
            # Now generate final filename with token count
            human_token_count = self._format_token_count(token_count)
            final_filename = f"{repo_name}_{version}_{human_token_count}.md"
            
            final_output_path = self.output_dir / final_filename
            
            # Rename temp file to final name
            temp_output_path.rename(final_output_path)
            
            # Update metadata
            repo_config = self.config['repositories'][repo_name]
            repo_config['metadata'] = {
                'last_updated': timestamp,
                'token_count': token_count,
                'character_count': char_count,
                'file_count': file_count,
                'last_file': final_filename,
                'profile': profile,
                'hash': self._get_file_hash(str(final_output_path))
            }
            
            # Save metadata
            self._save_config()
            self._save_ingestion_log(repo_name, profile, final_output_path, repo_config['metadata'])
            
            print(f"\n✅ Successfully ingested {repo_name}")
            print(f"   Output: {final_output_path}")
            print(f"   Tokens: {token_count:,}")
            print(f"   Characters: {char_count:,}")
            print(f"   Files: {file_count}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running gitingest: {e}")
            print(f"   stderr: {e.stderr}")
            # Clean up temp file if it exists
            if temp_output_path.exists():
                temp_output_path.unlink()
            sys.exit(1)
    
    def _save_ingestion_log(self, repo_name: str, profile: str, output_path: Path, metadata: dict):
        """Save ingestion log for tracking"""
        log_file = self.output_dir / "ingestion_log.json"
        
        # Load existing log
        if log_file.exists():
            with open(log_file, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        # Add new entry
        log.append({
            'timestamp': metadata['last_updated'],
            'repository': repo_name,
            'profile': profile,
            'file': str(output_path.name),
            'tokens': metadata['token_count'],
            'characters': metadata['character_count'],
            'files': metadata['file_count'],
            'hash': metadata['hash']
        })
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)
    
    def list_repos(self):
        """List all configured repositories"""
        print("\n=== Configured Repositories ===")
        for repo_name, repo_config in self.config['repositories'].items():
            print(f"\n{repo_name}:")
            print(f"  Description: {repo_config.get('description', 'N/A')}")
            print(f"  Source: {repo_config['source']}")
            print(f"  Exclusions: {len(repo_config.get('exclusions', []))} patterns")
            
            metadata = repo_config.get('metadata', {})
            if metadata and metadata.get('last_updated'):
                print(f"  Last ingested: {metadata['last_updated']}")
                print(f"  Last profile: {metadata.get('profile', 'unknown')}")
                print(f"  Tokens: {metadata.get('token_count', 0):,}")
                print(f"  Characters: {metadata.get('character_count', 0):,}")
    
    def list_profiles(self):
        """List all available profiles"""
        print("\n=== Available Profiles ===")
        for profile_name, profile_config in self.config['profiles'].items():
            print(f"\n{profile_name}:")
            print(f"  Description: {profile_config['description']}")
            print(f"  Additional exclusions: {len(profile_config.get('additional_exclusions', []))}")
    
    def list_ingested(self):
        """List all ingested files"""
        print(f"\n=== Ingested Files in {self.output_dir} ===")
        
        files = sorted(self.output_dir.glob("*.md"))
        if not files:
            print("No ingested files found.")
            return
        
        for file in files:
            stat = file.stat()
            size_mb = stat.st_size / (1024 * 1024)
            print(f"\n{file.name}:")
            print(f"  Size: {size_mb:.2f} MB ({stat.st_size:,} bytes)")
            print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    def clean_old(self, keep_latest: int = 3):
        """Clean old ingested files, keeping only the latest N per repository"""
        print(f"\n=== Cleaning old files (keeping latest {keep_latest} per repo) ===")
        
        # Group files by repository
        repo_files = {}
        for file in self.output_dir.glob("*.md"):
            # Extract repo name from filename
            parts = file.stem.split('_')
            if parts:
                repo = parts[0]
                if repo not in repo_files:
                    repo_files[repo] = []
                repo_files[repo].append(file)
        
        # Sort and clean each repository's files
        total_removed = 0
        total_size = 0
        
        for repo, files in repo_files.items():
            # Sort by modification time (newest first)
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Remove old files
            for file in files[keep_latest:]:
                size = file.stat().st_size
                print(f"  Removing: {file.name} ({size:,} bytes)")
                file.unlink()
                total_removed += 1
                total_size += size
        
        print(f"\n✅ Removed {total_removed} files ({total_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description='GitIngest Manager - Manage repository ingestion')
    parser.add_argument('command', choices=['ingest', 'list-repos', 'list-profiles', 'list-ingested', 'clean'],
                        help='Command to execute')
    parser.add_argument('--repo', '-r', help='Repository name for ingest command')
    parser.add_argument('--profile', '-p', default='standard', help='Profile to use (default: standard)')
    parser.add_argument('--version', '-v', help='Version tag for output file')
    parser.add_argument('--config', '-c', default='gitingest.yaml', help='Configuration file')
    parser.add_argument('--keep', '-k', type=int, default=3, help='Number of files to keep when cleaning')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = GitIngestManager(args.config)
    
    # Execute command
    if args.command == 'ingest':
        if not args.repo:
            print("Error: --repo is required for ingest command")
            sys.exit(1)
        manager.ingest(args.repo, args.profile, args.version)
    
    elif args.command == 'list-repos':
        manager.list_repos()
    
    elif args.command == 'list-profiles':
        manager.list_profiles()
    
    elif args.command == 'list-ingested':
        manager.list_ingested()
    
    elif args.command == 'clean':
        manager.clean_old(args.keep)


if __name__ == "__main__":
    main()
