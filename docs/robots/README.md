# FB-AI Robot Memory

This folder contains timestamped memory files created by the `fb-ai` command.

## Purpose

Every time `fb-ai` runs, it automatically creates a new markdown file here with:
- Timestamp of execution
- Command that was run
- Context and state of the execution
- Instructions for GitHub Copilot CLI
- Space for documenting next steps

## File Format

Files are named: `fb-ai_memory_YYYYMMDD_HHMMSS.md`

Example: `fb-ai_memory_20260110_175500.md`

## Usage

These files serve as:
1. **Execution History** - Track when and how fb-ai was run
2. **Context Preservation** - Maintain state across sessions
3. **AI Memory** - Help GitHub Copilot CLI remember project milestones
4. **Documentation** - Record important changes and decisions

## Integration

The fb-ai command at `.github/agents/fb-ai` automatically:
- Creates this directory if it doesn't exist
- Generates a new memory file on each run
- Includes instructions for milestone-based commits
