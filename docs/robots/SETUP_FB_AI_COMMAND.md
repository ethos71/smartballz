# Setting up smartballz Command (Optional)

To call `smartballz` from anywhere without `./`, you can add it to your PATH:

## Option 1: User bin directory (Recommended)

```bash
# Create wrapper script
mkdir -p ~/bin

cat << 'EOF' > ~/bin/smartballz
#!/bin/bash
# smartballz wrapper - calls the actual script from project directory
cd /home/dominick/workspace/smartballz && .github/prompts/smartballz "$@"
EOF

chmod +x ~/bin/smartballz

# Add to PATH (if not already there)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Now you can use just `smartballz` from anywhere!

## Option 2: Use from project root

If you don't want to set up PATH, just use it from the project root:

```bash
cd /home/dominick/workspace/smartballz
./smartballz
```

The symlink `smartballz` in the project root points to `.github/prompts/smartballz`.

## Verify Installation

```bash
which smartballz          # Should show ~/bin/smartballz
smartballz --help         # Should show help menu
smartballz --when         # Should check game times
```

## Notes

- The actual script is located at `.github/prompts/smartballz`
- The wrapper ensures it runs from the correct project directory
- Works from any directory once PATH is set up
