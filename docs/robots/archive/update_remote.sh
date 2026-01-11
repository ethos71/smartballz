#!/bin/bash
# Update git remote to smartballz repo

cd /home/dominick/workspace/smartballz

echo "=== Fixing symlink ==="
rm -f smartballz
ln -s .github/agents/smartballz smartballz

echo "=== Staging changes ==="
git add -A

echo "=== Committing ==="
git commit -m "Rename project to smartballz

- Renamed all fb-ai references to smartballz
- Updated branding to SmartBallz
- Fixed symlinks and directory structure"

echo "=== Updating remote URL ==="
git remote set-url origin https://github.com/ethos71/smartballz.git

echo "=== Verifying remote ==="
git remote -v

echo "=== Pushing to GitHub ==="
git push

echo ""
echo "✅ COMPLETE! Project renamed to smartballz"
