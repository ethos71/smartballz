# FB-AI Robot Memory

This folder contains timestamped memory files created by the `smartballz` command.

## Purpose

Every time `smartballz` runs, it automatically creates a new markdown file here with:
- Timestamp of execution
- Command that was run
- Context and state of the execution
- Instructions for GitHub Copilot CLI
- Space for documenting next steps

## File Format

Files are named: `smartballz_memory_YYYYMMDD_HHMMSS.md`

Example: `smartballz_memory_20260110_175500.md`

## Usage

These files serve as:
1. **Execution History** - Track when and how smartballz was run
2. **Context Preservation** - Maintain state across sessions
3. **AI Memory** - Help GitHub Copilot CLI remember project milestones
4. **Documentation** - Record important changes and decisions

## Integration

The smartballz command at `.github/agents/smartballz` automatically:
- Creates this directory if it doesn't exist
- Generates a new memory file on each run
- Includes instructions for milestone-based commits
