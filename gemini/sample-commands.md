# Gemini CLI Sample Commands

## Basic Commands

Remember to load environment variables first:
```bash
source .env
```

### Simple prompt
```bash
gemini -p "Hello, explain what you can do"
```

### Auto-confirm mode
```bash
gemini -y -p "analyze this repository structure"
```

### Architectural analysis with file reference
```bash
gemini -y -p "run this architectural analysis on this codebase: @large_gitingest.md" > gemini_plan.md
```

## Advanced Usage

### Code analysis
```bash
gemini -y -p "review this code for security issues: @src/main.py"
```

### Generate documentation
```bash
gemini -y -p "create API documentation for: @api/"
```

### Bug hunting
```bash
gemini -y -p "find potential bugs in: @src/ and suggest fixes"
```

### Test generation
```bash
gemini -y -p "generate unit tests for: @src/utils.py"
```

## File Reference Syntax

Use `@` to reference files or directories:
- `@filename.ext` - Reference a specific file
- `@directory/` - Reference all files in a directory
- `@*.py` - Reference all Python files in current directory

## Output Redirection

Save output to file:
```bash
gemini -y -p "analyze codebase" > analysis.md
```

Append to existing file:
```bash
gemini -y -p "additional analysis" >> analysis.md
```

## Interactive Mode

Just run `gemini` without arguments to enter interactive mode:
```bash
gemini
```

## Configuration Options

Use different models:
```bash
gemini --model gemini-1.5-pro -p "complex analysis task"
```

Adjust temperature:
```bash
gemini --temperature 0.9 -p "creative writing task"
```