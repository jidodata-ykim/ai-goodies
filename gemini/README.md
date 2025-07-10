# Gemini CLI Setup

Complete setup guide for using Gemini CLI with `.env` file configuration.

## Prerequisites

- Node.js version 20 or higher
- A Google API key from Google AI Studio

## Installation

### Option 1: Quick run (no installation required)
```bash
npx https://github.com/google-gemini/gemini-cli
```

### Option 2: Global installation (recommended)
```bash
pnpm install -g @google/gemini-cli
```

## API Key Setup

### Step 1: Get your API key

1. Go to [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the generated key

### Step 2: Create .env file (Recommended)

```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your API key
nano .env
```

Add your API key to the `.env` file:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 3: Load environment variables

Before running gemini commands, load the environment variables:
```bash
# Load environment variables from .env file
source .env
```

Or use a tool like `direnv` for automatic loading:
```bash
# Install direnv (if not already installed)
# Then create .envrc file
echo "source .env" > .envrc
direnv allow
```

## Configuration Setup

### Copy the config file to the right location:
```bash
# Create the gemini config directory
mkdir -p ~/.gemini

# Copy the config file
cp config.toml ~/.gemini/config.toml

# Edit the config file with your preferences
nano ~/.gemini/config.toml
```

## Usage Examples

### Load environment and run commands
```bash
# Load environment variables first
source .env

# Basic usage
gemini -p "explain this code"

# With auto-confirm flag
gemini -y -p "analyze this codebase"

# Architectural analysis example
gemini -y -p "run this architectural analysis on this codebase: @large_gitingest.md" > gemini_plan.md
```

## Authentication

On first run, Gemini CLI will prompt you to:
1. Choose a theme style
2. Select a login method (Google login or API key)

If you've set the environment variables correctly, it will automatically use your API key.

## Troubleshooting

- Make sure Node.js version is 20 or higher: `node --version`
- Verify your `.env` file exists and has the API key: `cat .env`
- Check if environment variables are loaded: `echo $GOOGLE_API_KEY`
- Make sure to run `source .env` before using gemini commands
- Check if gemini is globally installed: `which gemini`
- For rate limiting issues, consider upgrading to a paid Google AI Studio plan

## Files in this directory

- `.env.example` - Template for environment variables
- `config.toml` - Configuration file template for `~/.gemini/config.toml`
- `sample-commands.md` - Example commands and usage patterns