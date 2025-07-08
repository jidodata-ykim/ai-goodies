# AI Goodies

A collection of useful utilities and configurations for AI development workflows.

## Contents

### Clipboard Utilities

#### `tclip` - Tmux Clipboard Tool
A versatile clipboard management tool for tmux sessions that supports multiple operations:

- **Copy mode**: Copies piped input or file contents to the system clipboard
- **Paste mode**: Outputs clipboard contents (useful for piping to other commands)
- **Interactive mode**: Opens clipboard contents in your default editor for viewing/editing

**Usage:**
```bash
# Copy to clipboard
echo "Hello World" | tclip
cat file.txt | tclip

# Paste from clipboard
tclip -p
tclip -p > output.txt

# Interactive edit
tclip -i
```

#### `tsnip` - Code Snippet Formatter
Formats code snippets with syntax highlighting and line numbers, perfect for sharing code in documentation or chat.

**Features:**
- Automatic language detection
- Line numbering
- Syntax highlighting (when available)
- Clean markdown code block output

**Usage:**
```bash
# Format a file
tsnip script.py
tsnip -l javascript app.js

# Format from stdin
cat script.sh | tsnip -l bash

# Format and copy to clipboard
tsnip script.py | tclip
```

### Commands

The `commands/` directory contains a collection of useful Claude Code commands for enhanced development workflows. These commands demonstrate effective prompt engineering techniques and provide streamlined workflows for common development tasks.

**Available Commands:**
- `commit-fast.md` - Quick commit workflow for rapid development
- `commit.md` - Comprehensive commit process with proper formatting
- `issue-create.md` - Create well-structured GitHub issues
- `issue-understand.md` - Deep analysis of existing issues
- `pr-create.md` - Streamlined pull request creation
- `pr-review.md` - Comprehensive code review process
- `pr-update.md` - Update and maintain pull requests
- `task-implement.md` - Structured task implementation framework

These commands showcase effective prompt engineering patterns and can be used as templates for your own Claude Code workflows.

### Tmux Configuration

The `tmux.conf` file provides a modern, feature-rich tmux setup with:

- **Enhanced visuals**: Clean status bar with system information
- **Vim-style navigation**: Navigate panes with hjkl keys
- **Mouse support**: Click to select panes and windows
- **Better clipboard integration**: Seamless copy/paste with system clipboard
- **Sensible defaults**: 1-based indexing, automatic window renaming
- **Plugin support**: TPM (Tmux Plugin Manager) ready

Key bindings:
- `Ctrl-a` as prefix (instead of default `Ctrl-b`)
- `Prefix + |` for vertical split
- `Prefix + -` for horizontal split
- `Prefix + r` to reload configuration
- `Alt + h/j/k/l` for pane navigation without prefix

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jidodata-ykim/ai-goodies.git
cd ai-goodies
```

2. Make the scripts executable:
```bash
chmod +x tclip tsnip
```

3. Add the scripts to your PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/ai-goodies"
```

4. For tmux configuration:
```bash
# Backup existing config if any
[ -f ~/.tmux.conf ] && mv ~/.tmux.conf ~/.tmux.conf.bak

# Link the new configuration
ln -s /path/to/ai-goodies/tmux.conf ~/.tmux.conf

# Reload tmux configuration
tmux source-file ~/.tmux.conf
```

## Requirements

- **tmux**: Version 2.1 or higher recommended
- **xclip** or **xsel**: For clipboard operations on Linux
- **pbcopy/pbpaste**: Pre-installed on macOS
- **Python 3**: For syntax highlighting in tsnip (optional)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.