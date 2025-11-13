# Automatic Yahoo Roster Fetching

## Overview

The `fb-ai` command now **automatically fetches your latest roster from Yahoo Fantasy** every time it runs! This ensures your sit/start analysis always uses your current roster composition.

## How It Works

### Automatic Workflow

Every time you run `fb-ai`, the system:

1. **Connects to Yahoo Fantasy API** using OAuth credentials from `oauth2.json`
2. **Fetches your current MLB teams** from all leagues you're in
3. **Downloads the latest rosters** for each team
4. **Saves a timestamped snapshot** as `yahoo_fantasy_rosters_YYYYMMDD_HHMMSS.csv`
5. **Uses the roster** for sit/start analysis

### Your Leagues

The system automatically detects and fetches rosters from:
- **Monster Island** - "I Like BIG Bunts" team
- **Gotham City Baseball** - "Pure Uncut Adam West" team

### Season Detection

- Automatically uses the **current MLB season**
- If before March, uses the previous season
- No manual configuration needed

## File Locations

### OAuth Credentials
```
oauth2.json
```
- Yahoo API access token
- Automatically refreshed when expired
- Already configured and working

### Roster Snapshots
```
data/yahoo_fantasy_rosters_YYYYMMDD_HHMMSS.csv
```
- Historical record of roster changes
- Timestamped for tracking
- Used by sit/start analysis

### Example
```bash
data/yahoo_fantasy_rosters_20251112_181604.csv
```
- 61 players
- Both leagues combined
- Fetched on 2025-11-12 at 18:16:04

## Usage

### Daily Workflow

```bash
# Simply run fb-ai - roster fetch is automatic!
fb-ai

# Or for a specific date
fb-ai --date 2025-09-28

# Quick mode (skip weight tuning)
fb-ai --quick
```

### What Happens

```
⚾ FANTASY BASEBALL AI - SIT/START ANALYSIS
================================================================================

Mode: QUICK MODE (no weight tuning)
Estimated time: 1-2 minutes
Target date: 2025-09-28

================================================================================

🎯 Target Date: 2025-09-28

================================================================================
                          STEP 1: Update Data (Deltas)                          
================================================================================

Fetching latest MLB data and weather updates...

▶ MLB Delta Update...
  ✓ MLB Delta Update completed

▶ Weather Delta Update...
  ✓ Weather Delta Update completed

▶ Yahoo Roster Fetch...
  ✓ Found your teams:
    • I Like BIG Bunts (Monster Island)
    • Pure Uncut Adam West (Gotham City Baseball)
  ✓ Fetched 61 players
  ✓ Saved to: yahoo_fantasy_rosters_20251112_181604.csv
  ✓ Yahoo Roster Fetch completed

✓ Data updates completed successfully

================================================================================
                  STEP 2: Run All Factor Analyses (20 Factors)                  
================================================================================

...
```

## Technical Details

### API Integration

The system uses:
- **Yahoo Fantasy Sports API v2**
- **OAuth 2.0** authentication with automatic token refresh
- **JSON format** for all API responses

### Roster Detection

The scraper:
1. Gets all your MLB leagues
2. Finds teams where you're the manager (checks GUID)
3. Fetches complete rosters with positions
4. Combines into single CSV file

### Data Structure

CSV columns:
- `fantasy_team` - Team name ("I Like BIG Bunts" or "Pure Uncut Adam West")
- `player_name` - Player's full name
- `mlb_team` - MLB team abbreviation (NYY, BOS, etc.)
- `position` - Current position
- `eligible_positions` - All eligible positions
- `scraped_at` - Timestamp of when data was fetched

### Example Data

```csv
fantasy_team,player_name,mlb_team,position,eligible_positions,scraped_at
I Like BIG Bunts,Aaron Judge,NYY,OF,OF,2025-11-12T18:16:04.123456
Pure Uncut Adam West,Paul Skenes,PIT,SP,SP,2025-11-12T18:16:04.123456
```

## Troubleshooting

### Token Expired

If you see "Token expired":
```bash
# The system auto-refreshes, but if it fails:
rm oauth2.json
# Then re-authenticate by running fb-ai
```

### No Teams Found

If no teams are detected:
1. Check you're logged into Yahoo Fantasy
2. Verify oauth2.json exists and has valid credentials
3. Make sure you have active MLB teams

### Roster Not Found

If sit/start analysis says "No roster file found":
1. Check `data/yahoo_fantasy_rosters_*.csv` exists
2. Run yahoo scraper manually: `python src/scripts/scrape/yahoo_scrape.py`
3. Check for error messages in Step 1

## Manual Roster Fetch

You can also fetch rosters manually:

```bash
python src/scripts/scrape/yahoo_scrape.py
```

Output:
```
================================================================================
                       YAHOO FANTASY BASEBALL API CLIENT                        
================================================================================

✓ OAuth authentication successful!

Finding Your Teams:
  ✓ I Like BIG Bunts (in Monster Island)
  ✓ Pure Uncut Adam West (in Gotham City Baseball)

Fetching Rosters from 2 Team(s):

📊 Fetching 'I Like BIG Bunts'...
  ✓ Aaron Judge - NYY (OF)
  ✓ Elly De La Cruz - CIN (SS)
  ...

📊 Fetching 'Pure Uncut Adam West'...
  ✓ Paul Skenes - PIT (SP)
  ✓ Spencer Strider - ATL (SP)
  ...

✅ Exported 61 players to:
   data/yahoo_fantasy_rosters_20251112_181604.csv
   I Like BIG Bunts: 32 players
   Pure Uncut Adam West: 29 players
```

## Historical Rosters

All fetched rosters are saved with timestamps, allowing you to:
- Track roster changes over time
- Compare lineups from different dates
- Analyze trades and pickups
- Re-run historical analysis

Example:
```bash
# View roster from specific date
cat data/yahoo_fantasy_rosters_20251015_120000.csv

# Count rosters fetched
ls data/yahoo_fantasy_rosters_*.csv | wc -l

# See all rosters
ls -lht data/yahoo_fantasy_rosters_*.csv
```

## Benefits

### Always Current
- No manual roster updates needed
- Automatically includes trades, pickups, drops
- Reflects your actual lineup

### Historical Tracking
- Every fetch is saved
- Track roster evolution
- Analyze past decisions

### Multi-League Support
- Works with multiple leagues simultaneously
- Combines all your teams in one file
- Separate team attribution

### Zero Configuration
- Works out of the box
- No manual setup after initial OAuth
- Automatic season detection

## Summary

The `fb-ai` command now provides a **fully automated** workflow:

1. ✅ **Fetches your latest roster** from Yahoo
2. ✅ **Updates MLB data** (games, stats, weather)
3. ✅ **Runs all 20 factor analyses**
4. ✅ **Generates personalized recommendations**
5. ✅ **Saves historical snapshots**

Just run `fb-ai` and everything happens automatically!

---

**Last Updated:** 2025-11-12  
**Version:** 2.0 (Automatic Roster Fetching)
