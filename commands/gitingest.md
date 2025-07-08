# GitIngest: Repository Token Optimization Workflow

## Purpose
Intelligently ingest GitHub repositories while optimizing token count by excluding non-essential directories based on project type and language, to stay under 500k tokens.

## Prerequisites

1. **Install Required Tools**
   ```bash
   # Check if dust is installed for directory size analysis
   dust --version || (echo "Install dust: cargo install du-dust" && exit 1)
   
   # Check if token-counter is installed for token estimation
   token-counter --version || (echo "Install token-counter: cargo install token-counter" && exit 1)
   ```

## Workflow Steps

1. **Add to .gitignore and Clone Repository**
   ```bash
   cd /mnt/data/harness/gitingest
   # Add the repo directory to .gitignore BEFORE cloning to prevent watchman/jj tracking
   echo "gitingest/<REPO_NAME>/" >> /mnt/data/harness/.gitignore
   git clone <GITHUB_URL> <REPO_NAME>
   ```

2. **Detect Project Language and Type**
   Use common indicators to determine the primary language(s):
   ```bash
   # Check for language-specific files
   find <REPO_NAME> -maxdepth 2 -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" -o -name "*.rs" -o -name "*.cpp" -o -name "*.c" | head -5
   
   # Check for package managers and config files
   ls <REPO_NAME>/ | grep -E "(package.json|requirements.txt|Cargo.toml|go.mod|pom.xml|build.gradle|composer.json|Gemfile)"
   ```

3. **Analyze Directory Sizes**
   Use `dust` to identify large directories that can be excluded:
   ```bash
   dust -d 2 <REPO_NAME>/ | sort -hr | head -20
   ```
   
   **Language-Agnostic Exclusions (Common to all projects):**
   - Documentation folders (docs/, documentation/, wiki/)
   - Build artifacts (build/, dist/, out/, target/)
   - Package managers (node_modules/, vendor/, .venv/, venv/)
   - IDE files (.vscode/, .idea/, .eclipse/)
   - Test data directories (test_data/, fixtures/, __pycache__/)
   - Version control (.git/, .svn/, .hg/)
   - Assets (static/, assets/, public/, images/)
   
   **Language-Specific Exclusions:**
   - **Python**: *.pyc, __pycache__/, *.egg-info/, .pytest_cache/
   - **JavaScript/TypeScript**: node_modules/, dist/, coverage/, .next/, .nuxt/
   - **Java**: target/, *.class, *.jar, .gradle/
   - **C/C++**: *.o, *.so, *.dll, cmake-build-*/
   - **Rust**: target/, Cargo.lock (for libraries)
   - **Go**: vendor/, *.exe
   - **PHP**: vendor/, composer.lock
   - **Ruby**: .bundle/, vendor/bundle/
   
   **Additional Exclusions if needed:**
   - Examples/demos (examples/, demos/, samples/)
   - Localization files (i18n/, locales/, translations/)
   - Configuration templates (templates/, config/)

4. **Initial Token Count**
   ```bash
   gitingest <REPO_NAME> 
   ```
   Record the original token count. If it's already below 400k tokens, just gitingest the full repo, add the details to gitingest.yaml, but nothing needs to be excluded.
   
   **Alternative using token-counter:**
   ```bash
   # Count tokens in generated file
   gitingest <REPO_NAME> -o temp_output.md
   token-counter temp_output.md
   ```

5. **Configure Exclusions**
   Update `gitingest.yaml` with identified exclusions based on project type:
   
   **For Python projects:**
   ```yaml
   repositories:
     <REPO_NAME>:
       source: "<REPO_NAME>"
       exclusions:
         - "docs/"
         - "tests/fixtures/"
         - "examples/"
         - "__pycache__/"
         - "*.pyc"
         - "build/"
         - "dist/"
         - "*.egg-info/"
   ```
   
   **For JavaScript/TypeScript projects:**
   ```yaml
   repositories:
     <REPO_NAME>:
       source: "<REPO_NAME>"
       exclusions:
         - "docs/"
         - "node_modules/"
         - "dist/"
         - "build/"
         - "coverage/"
         - "*.min.js"
         - "*.min.css"
         - ".next/"
         - ".nuxt/"
   ```
   
   **For Java projects:**
   ```yaml
   repositories:
     <REPO_NAME>:
       source: "<REPO_NAME>"
       exclusions:
         - "docs/"
         - "target/"
         - "*.class"
         - "*.jar"
         - ".gradle/"
         - "build/"
   ```
   
   **For Multi-language projects:**
   ```yaml
   repositories:
     <REPO_NAME>:
       source: "<REPO_NAME>"
       exclusions:
         - "docs/"
         - "node_modules/"
         - "__pycache__/"
         - "target/"
         - "build/"
         - "dist/"
         - "vendor/"
   ```

6. **Generate Optimized Ingestion**
   ```bash
   uv run python utils/gitingest_manager.py ingest --repo <REPO_NAME>
   ```
   This will:
   - Apply exclusions from gitingest.yaml
   - Generate timestamped .md file in ingested/
   - Display token count statistics using token-counter
   - Work with any programming language

7. **Verify Token Reduction**
   The script will output:
   - Original token count (via token-counter)
   - Optimized token count
   - Reduction percentage
   - Full path to generated .md file
   - Language detection and exclusion summary

## Example Usage

**Python Project (SigNoz):**
```bash
# 1. Check prerequisites
dust --version && token-counter --version

# 2. Add to .gitignore and clone a repository
cd /mnt/data/harness/gitingest
echo "gitingest/signoz/" >> /mnt/data/harness/.gitignore
git clone https://github.com/SigNoz/signoz signoz

# 3. Detect language
find signoz -maxdepth 2 -name "*.py" -o -name "*.js" -o -name "*.ts" | head -5
ls signoz/ | grep -E "(package.json|requirements.txt|Cargo.toml)"

# 4. Analyze with dust
dust -d 2 signoz/ | sort -hr | head -20
# Identifies: docs/ (450MB), tests/data/ (200MB), frontend/ (150MB)

# 5. Check initial estimated tokens
gitingest signoz -o temp.md && token-counter temp.md

# 6. Update gitingest.yaml with Python + JS exclusions
# 7. Run optimization
uv run python utils/gitingest_manager.py ingest --repo signoz

# Output:
# ✓ Generated: /mnt/data/harness/gitingest/ingested/signoz_v0.6.1_437k.md
# 📊 Token Statistics:
#   Original: 4,847,392 tokens
#   Optimized: 437,291 tokens
#   Reduction: 82.9%
```

**TypeScript Project:**
```bash
# 1. Clone and analyze
cd /mnt/data/harness/gitingest
echo "gitingest/vscode/" >> /mnt/data/harness/.gitignore
git clone https://github.com/microsoft/vscode vscode

# 2. Detect TypeScript project
ls vscode/ | grep -E "(package.json|tsconfig.json)"

# 3. Analyze and configure exclusions for TypeScript
dust -d 2 vscode/ | sort -hr | head -20
# Focus on: node_modules/, out/, build/, extensions/

# 4. Run optimization
uv run python utils/gitingest_manager.py ingest --repo vscode
```

## Pro Tips
- **Language Detection**: Use file extensions and package managers to identify primary languages
- **Prioritize Core Code**: Keep source code files and essential configurations
- **Exclude Generated Files**: Remove compiled, built, or generated content
- **Package Managers**: Always exclude package directories (node_modules/, vendor/, etc.)
- **Wildcard Patterns**: Use patterns like "**/*.min.js" for efficiency
- **Token Estimation**: Use token-counter for accurate token counting
- **Multi-language Projects**: Combine exclusions from different language ecosystems
- **Test Data**: Exclude large test fixtures and sample data
- **Documentation**: Consider excluding extensive documentation if not needed for analysis

## Quick Commands

**Language Detection:**
```bash
# Detect primary language
find <REPO_NAME> -maxdepth 2 -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -5
```

**Exclusion Suggestions:**
```bash
# General exclusions (any language)
dust -d 2 <REPO_NAME>/ | sort -hr | head -10 | awk '{print $2}' | grep -E "(docs|test|build|dist|node_modules|vendor|target)" | sed 's|^<REPO_NAME>/|  - "|; s|$|/"|'

# Language-specific exclusions
dust -d 2 <REPO_NAME>/ | sort -hr | head -10 | awk '{print $2}' | grep -vE "\.(py|js|ts|java|go|rs|cpp|c|h)$" | sed 's|^<REPO_NAME>/|  - "|; s|$|/"|'
```

**Token Count Verification:**
```bash
# Quick token count after optimization
gitingest <REPO_NAME> -o temp.md && token-counter temp.md && rm temp.md
```

## Language-Specific Exclusion Templates

**Python Projects:**
```yaml
exclusions:
  - "docs/"
  - "tests/fixtures/"
  - "__pycache__/"
  - "*.pyc"
  - "build/"
  - "dist/"
  - "*.egg-info/"
  - ".pytest_cache/"
  - ".coverage"
```

**JavaScript/Node.js Projects:**
```yaml
exclusions:
  - "node_modules/"
  - "dist/"
  - "build/"
  - "coverage/"
  - "*.min.js"
  - "*.min.css"
  - ".next/"
  - ".nuxt/"
  - "public/"
```

**Java Projects:**
```yaml
exclusions:
  - "target/"
  - "*.class"
  - "*.jar"
  - ".gradle/"
  - "build/"
  - "out/"
```

**Rust Projects:**
```yaml
exclusions:
  - "target/"
  - "Cargo.lock"  # Only for libraries
  - "*.rlib"
```

**Go Projects:**
```yaml
exclusions:
  - "vendor/"
  - "*.exe"
  - "bin/"
```
