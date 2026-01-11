#!/bin/bash
# Complete renaming to smartballz

set -e

cd /home/dominick/workspace/smartballz

echo "=== Fixing symlink ==="
rm -f smartballz
ln -s .github/agents/smartballz smartballz
ls -la smartballz

echo "=== Staging all changes ==="
git add -A

echo "=== Showing changes ==="
git status --short | head -40

echo "=== Committing changes ==="
git commit -m "Rename project from fantasy-baseball-ai to smartballz

Major Changes:
- Renamed agent: fb-ai → smartballz
- Renamed prompt: fb-ai → smartballz  
- Renamed executable: fb-ai → smartballz
- Updated all file references
- Updated branding: Fantasy Baseball AI → SmartBallz
- Renamed project directory

Next step: Rename GitHub repo manually"

echo "=== Current remote ==="
git remote -v

echo ""
echo "✅ LOCAL RENAMING COMPLETE"
echo ""
echo "Next steps:"
echo "1. Go to GitHub: https://github.com/ethos71/fantasy-baseball-ai"
echo "2. Click Settings → Rename repository"
echo "3. Change to: smartballz"
echo "4. Then run: git remote set-url origin https://github.com/ethos71/smartballz.git"
echo "5. Push: git push"
