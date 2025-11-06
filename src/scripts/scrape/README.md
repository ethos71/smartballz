# Data Scrapers

This directory contains all data collection scripts that fetch information from various sources.

## Available Scrapers

### MLB Scraper (`mlb_scrape.py`)

**Purpose:** Comprehensive MLB statistics scraper using MLB's official Stats API.

**What it does:**
- Fetches all 30 MLB teams with complete details
- Retrieves game schedules for current year + last 3 years (2025, 2024, 2023, 2022)
- Downloads all player rosters (5,969+ player-season records)
- Exports everything to CSV for analysis

**Data Source:** [MLB Stats API](https://statsapi.mlb.com/api)

**Usage:**
```bash
python src/scripts/scrape/mlb_scrape.py
```

**Output Files:**
- `data/mlb_all_teams.csv` - All 30 MLB teams
- `data/mlb_YYYY_schedule.csv` - Schedules by year (4 files)
- `data/mlb_all_players_YYYY.csv` - Players by year (4 files)
- `data/mlb_all_players_complete.csv` - Complete player database

**Runtime:** ~5-8 minutes (full scrape)

---

### MLB Delta Scraper (`mlb_delta_scrape.py`)

**Purpose:** Fast incremental updates for recent MLB data.

**What it does:**
- Fetches only NEW games since last update
- Updates current player rosters
- Appends to existing CSV files (doesn't overwrite)
- Much faster than full scrape

**Usage:**
```bash
python src/scripts/scrape/mlb_delta_scrape.py
```

**When to use:**
- Daily updates during season
- Quick roster checks
- Recent game additions

**Runtime:** ~30 seconds

---

### Weather Scraper (`weather_scrape.py`)

**Purpose:** ML-based weather prediction for all 30 MLB stadiums.

**What it does:**
- Fetches current weather conditions at all MLB stadium locations
- Uses Random Forest classifier to predict Rainy/Sunny conditions
- Collects comprehensive weather metrics:
  - Temperature, humidity, pressure
  - Wind speed, direction, and gusts
  - Cloud cover and precipitation
  - ML prediction with confidence score

**Data Source:** [Open-Meteo Weather API](https://open-meteo.com/) (free, no API key required)

**Based on:** [WeatherPrediction_ML_Model](https://github.com/FELIX-GEORGE/WeatherPrediction_ML_Model)

**Usage:**
```bash
python src/scripts/scrape/weather_scrape.py
```

**Output Files:**
- `data/mlb_stadium_weather.csv` - Current weather at all 30 stadiums

**Runtime:** ~1-2 minutes

**Weather Metrics:**
- Temperature (°C)
- Humidity (%)
- Atmospheric Pressure (hPa)
- Wind Speed (km/h)
- Wind Direction (degrees and cardinal: N, NE, E, SE, S, SW, W, NW)
- Wind Gusts (km/h)
- Cloud Cover (%)
- Precipitation (mm)
- ML Prediction (Rainy/Sunny)
- Confidence Score

---

### Weather Delta Scraper (`weather_delta_scrape.py`)

**Purpose:** Ultra-fast weather updates for all stadiums.

**What it does:**
- Fetches current weather for all 30 stadiums
- Overwrites weather CSV with fresh data
- Quickest way to get latest conditions

**Usage:**
```bash
python src/scripts/scrape/weather_delta_scrape.py
```

**When to use:**
- Pre-game weather checks
- Daily condition updates
- Quick weather snapshots

**Runtime:** ~15 seconds

---

### Yahoo Fantasy Scraper (`yahoo_scrape.py`)

**Purpose:** Fetches your Yahoo Fantasy Baseball roster data.

**What it does:**
- Authenticates with Yahoo Fantasy Sports API via browser OAuth
- Fetches roster for your specified team names
- Exports player list with IDs and positions

**Prerequisites:**
1. Yahoo API credentials in `oauth2.json`:
   ```json
   {
     "consumer_key": "your_client_id",
     "consumer_secret": "your_client_secret"
   }
   ```

2. Browser path in `.env`:
   ```
   BROWSER_PATH=/usr/bin/google-chrome
   ```

**Usage:**
```bash
python src/scripts/scrape/yahoo_scrape.py
```

**Output Files:**
- `data/yahoo_fantasy_rosters_YYYYMMDD.csv` - Your fantasy team rosters

**Runtime:** ~20-30 seconds (includes browser authentication)

**Configuration:**
- Team names configured in the script (default: "I like big bunts" and "Pure uncut adam west")
- OAuth tokens cached for future use

---

## Quick Reference

### Full Data Refresh (First Time)
```bash
# Run all scrapers for complete data collection
python src/scripts/scrape/mlb_scrape.py
python src/scripts/scrape/weather_scrape.py
python src/scripts/scrape/yahoo_scrape.py
```

### Daily Updates (Recommended)
```bash
# Fast incremental updates
python src/scripts/scrape/mlb_delta_scrape.py
python src/scripts/scrape/weather_delta_scrape.py
python src/scripts/scrape/yahoo_scrape.py
```

### Automated Usage
The main orchestrator `src/fb_ai.py` automatically manages all scrapers:
- `python src/fb_ai.py --refresh` runs full scrapers
- `python src/fb_ai.py` runs delta scrapers

---

## Common Issues

### MLB Scraper
- **Slow performance:** Normal for first run (5-8 minutes)
- **Missing data:** Check MLB Stats API status
- **Empty CSV:** Verify internet connection

### Weather Scraper
- **API timeout:** Open-Meteo rate limits apply (retry after 1 minute)
- **Missing coordinates:** Stadium locations hardcoded in script

### Yahoo Scraper
- **Authentication failed:** Check `oauth2.json` credentials
- **Browser not opening:** Verify `BROWSER_PATH` in `.env`
- **Token expired:** Delete cached token, re-authenticate
