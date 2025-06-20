#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BLUE}${BOLD}Git Checkpoint Creator v2${NC}"
echo "========================="

# Function to check if we're in a git repo
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}✗ Not in a git repository!${NC}"
        exit 1
    fi
}

# Function to check if there's a remote configured
check_remote() {
    if ! git remote | grep -q .; then
        echo -e "${RED}✗ No remote repository configured!${NC}"
        echo -e "${YELLOW}Add a remote with: git remote add origin <url>${NC}"
        exit 1
    fi
}

# Function to get the default remote
get_default_remote() {
    # Try to get the remote for the current branch
    local current_branch=$(git branch --show-current)
    local remote=$(git config --get branch.$current_branch.remote || echo "")
    
    if [ -z "$remote" ]; then
        # Fallback to origin if it exists
        if git remote | grep -q "^origin$"; then
            remote="origin"
        else
            # Use the first available remote
            remote=$(git remote | head -n1)
        fi
    fi
    
    echo "$remote"
}

# Function to get a human-readable name for the checkpoint
get_checkpoint_alias() {
    local default_name="$1"
    local alias_name=""
    
    # Check if an alias was provided as argument
    if [ -n "$2" ]; then
        alias_name="$2"
    else
        # Prompt for alias name
        echo -e "\n${CYAN}Enter a human-readable name for this checkpoint${NC}"
        echo -e "${CYAN}(press Enter to use timestamp only):${NC}"
        read -r alias_name
    fi
    
    # Clean up the alias name (remove spaces and special chars)
    if [ -n "$alias_name" ]; then
        alias_name=$(echo "$alias_name" | tr ' ' '-' | tr -cd '[:alnum:]-_')
        echo "${default_name}-${alias_name}"
    else
        echo "$default_name"
    fi
}

# Function to update or create the lastcheck tag
update_lastcheck() {
    local checkpoint_branch="$1"
    local remote="$2"
    
    echo -e "\n${BLUE}Updating 'lastcheck' reference...${NC}"
    
    # Delete existing lastcheck tag (both local and remote)
    git tag -d lastcheck 2>/dev/null || true
    git push $remote :refs/tags/lastcheck 2>/dev/null || true
    
    # Create new lastcheck tag pointing to the checkpoint
    git tag -a lastcheck "$checkpoint_branch" -m "Last checkpoint: $checkpoint_branch"
    
    # Push the tag
    if git push $remote lastcheck; then
        echo -e "${GREEN}✓ 'lastcheck' tag updated${NC}"
    else
        echo -e "${YELLOW}⚠ Could not push 'lastcheck' tag${NC}"
    fi
}

# Function to save checkpoint metadata
save_checkpoint_metadata() {
    local checkpoint_name="$1"
    local alias_part="$2"
    local git_dir=$(git rev-parse --git-dir)
    local metadata_file="${git_dir}/checkpoint_metadata"
    
    # Create metadata entry
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local commit_hash=$(git rev-parse "$checkpoint_name")
    
    # Ensure directory exists and append to metadata file
    touch "$metadata_file" 2>/dev/null || true
    echo "${checkpoint_name}|${alias_part}|${timestamp}|${commit_hash}" >> "$metadata_file"
}

# Function to list checkpoints with their aliases
list_checkpoints() {
    echo -e "\n${BLUE}${BOLD}Recent Checkpoints:${NC}"
    echo -e "${BLUE}==================${NC}"
    
    local git_dir=$(git rev-parse --git-dir)
    local metadata_file="${git_dir}/checkpoint_metadata"
    local remote=$(get_default_remote)
    
    # Get all checkpoint branches from remote
    git fetch $remote 'refs/heads/checkpoint-*:refs/remotes/'$remote'/checkpoint-*' 2>/dev/null || true
    
    # List last 10 checkpoints
    if [ -f "$metadata_file" ]; then
        echo -e "\n${CYAN}Name${NC} | ${MAGENTA}Alias${NC} | ${YELLOW}Date${NC}"
        echo "----------------------------------------"
        tail -10 "$metadata_file" | while IFS='|' read -r name alias timestamp hash; do
            if [ -n "$alias" ]; then
                printf "${CYAN}%-30s${NC} | ${MAGENTA}%-20s${NC} | ${YELLOW}%s${NC}\n" "$name" "$alias" "$timestamp"
            else
                printf "${CYAN}%-30s${NC} | ${MAGENTA}%-20s${NC} | ${YELLOW}%s${NC}\n" "$name" "(no alias)" "$timestamp"
            fi
        done
    else
        # Fallback to listing from git
        git branch -r | grep checkpoint | tail -10 || echo "No checkpoints found"
    fi
    
    # Show lastcheck
    echo -e "\n${GREEN}Last checkpoint:${NC}"
    git show-ref --tags | grep lastcheck || echo "  No 'lastcheck' tag set"
}

# Main function
main() {
    # Handle special commands
    if [ "$1" = "list" ] || [ "$1" = "-l" ] || [ "$1" = "--list" ]; then
        check_git_repo
        list_checkpoints
        exit 0
    fi
    
    # Check prerequisites
    check_git_repo
    check_remote
    
    # Get current branch and status
    CURRENT_BRANCH=$(git branch --show-current)
    echo -e "${BLUE}Current branch:${NC} $CURRENT_BRANCH"
    
    # Check if there are any changes to checkpoint
    if [[ -z $(git status -s) ]]; then
        echo -e "\n${GREEN}✓ No uncommitted changes to checkpoint${NC}"
        list_checkpoints
        exit 0
    fi
    
    # Show uncommitted changes
    echo -e "\n${YELLOW}Uncommitted changes detected:${NC}"
    git status -s | head -20
    local change_count=$(git status -s | wc -l)
    if [ "$change_count" -gt 20 ]; then
        echo -e "${YELLOW}... and $((change_count - 20)) more files${NC}"
    fi
    
    # Create checkpoint branch name with timestamp
    BASE_CHECKPOINT_NAME="checkpoint-$(date +%Y%m%d-%H%M%S)"
    CHECKPOINT_BRANCH=$(get_checkpoint_alias "$BASE_CHECKPOINT_NAME" "$1")
    
    # Extract alias part if exists
    ALIAS_PART=""
    if [ "$CHECKPOINT_BRANCH" != "$BASE_CHECKPOINT_NAME" ]; then
        ALIAS_PART="${CHECKPOINT_BRANCH#$BASE_CHECKPOINT_NAME-}"
    fi
    
    echo -e "\n${BLUE}Checkpoint branch:${NC} $CHECKPOINT_BRANCH"
    if [ -n "$ALIAS_PART" ]; then
        echo -e "${BLUE}Alias:${NC} $ALIAS_PART"
    fi
    
    # Check for large files before staging
    echo -e "\n${BLUE}Checking for large files...${NC}"
    LARGE_FILES=$(find . -type f -size +10M ! -path "./.git/*" -exec ls -lh {} + 2>/dev/null | awk '{print $5 "\t" $9}' | sort -hr | head -10)
    
    if [ -n "$LARGE_FILES" ]; then
        echo -e "${YELLOW}⚠ Warning: Found large files (>10MB):${NC}"
        echo "$LARGE_FILES" | while read line; do
            echo -e "  ${YELLOW}$line${NC}"
        done
        echo -e "${YELLOW}These files might slow down the checkpoint process.${NC}"
        echo -e "${YELLOW}Consider adding them to .gitignore if they shouldn't be tracked.${NC}"
        echo -e "\n${CYAN}Continue anyway? (y/N):${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo -e "${RED}Checkpoint cancelled.${NC}"
            exit 1
        fi
    fi
    
    # Stage all changes
    echo -e "\n${BLUE}Staging all changes...${NC}"
    git add -A
    
    # Create commit message
    COMMIT_MSG="Checkpoint $(date +%Y-%m-%d_%H-%M-%S)"
    if [ -n "$ALIAS_PART" ]; then
        COMMIT_MSG="$COMMIT_MSG - $ALIAS_PART"
    fi
    
    # Create temporary commit
    echo -e "${BLUE}Creating temporary commit...${NC}"
    git commit -m "$COMMIT_MSG" --no-verify -m "Automated checkpoint from branch: $CURRENT_BRANCH"
    
    # Create branch pointing to the commit
    echo -e "${BLUE}Creating checkpoint branch...${NC}"
    git branch "$CHECKPOINT_BRANCH"
    
    # Save metadata
    save_checkpoint_metadata "$CHECKPOINT_BRANCH" "$ALIAS_PART"
    
    # Reset main to preserve working state
    echo -e "${BLUE}Restoring working directory state...${NC}"
    git reset HEAD~1
    
    # Get the default remote
    REMOTE=$(get_default_remote)
    echo -e "${BLUE}Using remote:${NC} $REMOTE"
    
    # Push checkpoint branch
    echo -e "\n${BLUE}Pushing checkpoint to remote...${NC}"
    if git push $REMOTE "$CHECKPOINT_BRANCH"; then
        echo -e "${GREEN}✓ Checkpoint pushed successfully!${NC}"
        
        # Update lastcheck tag
        update_lastcheck "$CHECKPOINT_BRANCH" "$REMOTE"
        
        # Get the remote URL for display
        REMOTE_URL=$(git remote get-url $REMOTE)
        echo -e "\n${GREEN}Checkpoint created:${NC}"
        echo -e "  Branch: $CHECKPOINT_BRANCH"
        if [ -n "$ALIAS_PART" ]; then
            echo -e "  Alias: $ALIAS_PART"
        fi
        echo -e "  Remote: $REMOTE_URL"
        
        echo -e "\n${GREEN}✓ Checkpoint complete!${NC}"
        echo -e "${BLUE}To view this checkpoint:${NC} git checkout $CHECKPOINT_BRANCH"
        echo -e "${BLUE}To view last checkpoint:${NC} git checkout lastcheck"
        echo -e "${BLUE}To list all checkpoints:${NC} $0 list"
        
        echo -e "\n${YELLOW}Your working directory is preserved with uncommitted changes.${NC}"
    else
        echo -e "${RED}✗ Failed to push checkpoint${NC}"
        echo -e "${YELLOW}Note: Local checkpoint branch '$CHECKPOINT_BRANCH' was created but not pushed.${NC}"
        exit 1
    fi
}

# Show help if requested
if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    echo -e "\n${CYAN}Usage:${NC}"
    echo -e "  $0 [alias]          Create checkpoint with optional alias"
    echo -e "  $0 list            List recent checkpoints"
    echo -e "  $0 -h              Show this help"
    echo -e "\n${CYAN}Examples:${NC}"
    echo -e "  $0                 Create checkpoint with timestamp only"
    echo -e "  $0 \"before-refactor\"  Create checkpoint with alias"
    echo -e "  $0 azure-cli-done   Create checkpoint with alias (no quotes needed for single words)"
    echo -e "\n${CYAN}Special References:${NC}"
    echo -e "  lastcheck          Always points to the most recent checkpoint"
    echo -e "                     Use: git checkout lastcheck"
    exit 0
fi

# Run main function
main "$@"
