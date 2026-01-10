# Creating a Demo GIF for the Dashboard

## Manual Method (Easiest)

1. **Take Screenshots:**
   - Open the dashboard: http://localhost:8501
   - Take screenshots of key sections (press PrintScreen or use Snipping Tool)
   - Save as: `dashboard-01.png`, `dashboard-02.png`, etc. in `docs/screenshots/`

2. **Create GIF from Screenshots:**
   ```bash
   # Install imagemagick if needed
   sudo apt-get install imagemagick
   
   # Create GIF from screenshots
   cd docs/screenshots
   convert -delay 200 -loop 0 dashboard-*.png demo.gif
   
   # Optimize GIF size
   convert demo.gif -fuzz 10% -layers Optimize demo-optimized.gif
   ```

3. **Add to README:**
   ```markdown
   ![Dashboard Demo](docs/screenshots/demo-optimized.gif)
   ```

## What to Capture

### Screenshot 1: Dashboard Overview
- Shows the summary metrics at the top
- Navigation sidebar visible
- Clean, professional look

### Screenshot 2: Sit/Start Recommendations  
- Current roster table with recommendations
- Green (Start) and Red (Sit) indicators visible

### Screenshot 3: Player Breakdown
- Select a player
- Show all 20 factor scores
- Demonstrates depth of analysis

### Screenshot 4: Waiver Wire
- Top waiver wire targets
- Shows schedule analysis
- Coors Field advantage plays

### Screenshot 5: Factor Analysis
- One of the detailed factor analysis views
- Shows data filtering/sorting capability

## Tips for Best Results

- Use full browser window (not maximized - about 1400px wide)
- Ensure data is loaded before screenshot
- Clear, readable font size
- No personal information visible
- Clean, professional appearance

## Alternative: Screen Recording

If you have OBS Studio or similar:
1. Record 30-60 second walkthrough
2. Export as MP4
3. Convert to GIF:
   ```bash
   ffmpeg -i recording.mp4 -vf "fps=10,scale=1000:-1:flags=lanczos" -c:v gif demo.gif
   ```

---

The manual screenshot method gives the best quality/size ratio for GitHub READMEs!
