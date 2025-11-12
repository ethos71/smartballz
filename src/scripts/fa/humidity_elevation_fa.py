#!/usr/bin/env python3
"""
Humidity & Elevation Factor Analysis

Analyzes how humidity and ballpark elevation affect ball flight and player performance.

Key Concepts:
- High Humidity + High Temperature = Ball travels further (sticky air carries ball)
- High Elevation (thin air) = Ball travels significantly further
- Coors Field effect: 5,200 ft elevation = ~9% more HRs
- Humidity affects both distance and movement (changeups, breaking balls)

Scientific Basis:
- At 90°F with 90% humidity vs 10%, ball travels ~5-8 feet further
- Every 1,000 ft elevation = ~3% increase in ball flight distance
- Combined effect can add 15-20 feet to fly balls

Output: Adjustment scores for hitter advantage based on conditions
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class HumidityElevationAnalyzer:
    """Analyze humidity and elevation effects on performance"""
    
    # MLB Ballpark Elevations (in feet)
    BALLPARK_ELEVATIONS = {
        'Coors Field': 5200,           # Denver - Highest
        'Chase Field': 1086,            # Arizona
        'Globe Life Field': 550,        # Texas
        'Kauffman Stadium': 910,        # Kansas City
        'Busch Stadium': 535,           # St. Louis
        'Guaranteed Rate Field': 595,   # Chicago White Sox
        'Wrigley Field': 595,           # Chicago Cubs
        'T-Mobile Park': 10,            # Seattle - Sea level
        'Oracle Park': 10,              # San Francisco - Sea level
        'Petco Park': 20,               # San Diego - Sea level
        'Tropicana Field': 10,          # Tampa Bay
        'Fenway Park': 20,              # Boston
        'Yankee Stadium': 55,           # New York Yankees
        'Citi Field': 10,               # New York Mets
        'Citizens Bank Park': 10,       # Philadelphia
        'Nationals Park': 25,           # Washington
        'Truist Park': 1050,            # Atlanta
        'loanDepot park': 10,           # Miami
        'Oriole Park': 33,              # Baltimore
        'Progressive Field': 660,       # Cleveland
        'Comerica Park': 585,           # Detroit
        'Target Field': 840,            # Minnesota
        'Rogers Centre': 300,           # Toronto
        'American Family Field': 635,   # Milwaukee
        'Great American Ball Park': 550, # Cincinnati
        'PNC Park': 730,                # Pittsburgh
        'Dodger Stadium': 340,          # Los Angeles
        'Angel Stadium': 160,           # Los Angeles Angels
        'Oakland Coliseum': 25,         # Oakland
        'Minute Maid Park': 22,         # Houston
    }
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
    
    def calculate_humidity_factor(self, humidity_pct, temperature_c):
        """Calculate hitting advantage from humidity"""
        # Convert to Fahrenheit
        temp_f = (temperature_c * 9/5) + 32
        
        # Humidity effect is stronger at higher temperatures
        # Base calculation: At 90°F, 90% humidity vs 10% adds ~6 feet
        # Scale by temperature
        
        if temp_f < 50:
            # Cold weather - humidity has minimal effect
            humidity_boost = 0.0
        elif temp_f >= 90:
            # Hot weather - maximum humidity effect
            # 90% humidity = +1.0, 10% humidity = -1.0
            humidity_boost = (humidity_pct - 50) / 40  # Scale -1.0 to +1.0
        else:
            # Moderate temps - scale effect proportionally
            temp_factor = (temp_f - 50) / 40  # 0 at 50°F, 1 at 90°F
            humidity_boost = ((humidity_pct - 50) / 40) * temp_factor
        
        return np.clip(humidity_boost, -1.0, 1.0)
    
    def calculate_elevation_factor(self, stadium_name):
        """Calculate hitting advantage from elevation"""
        elevation = self.BALLPARK_ELEVATIONS.get(stadium_name, 500)  # Default moderate
        
        # Research shows ~3% distance increase per 1000 ft
        # Normalize to -1.0 to +1.0 range where Coors = 1.0
        
        if elevation >= 5000:  # Coors territory
            return 1.0
        elif elevation >= 1000:  # Moderate elevation
            return (elevation - 500) / 4500  # Scale 500-5200 to 0-1
        elif elevation < 100:  # Sea level
            return -0.3  # Slight disadvantage vs league average
        else:
            return (elevation - 100) / 900 * 0.3  # Scale to slight advantage
    
    def calculate_air_density_score(self, humidity_pct, temperature_c, elevation_ft):
        """Calculate combined air density effect"""
        # Lower air density = ball travels further
        
        # Temperature effect (hot = less dense)
        temp_f = (temperature_c * 9/5) + 32
        temp_factor = (temp_f - 60) / 30  # Normalized around 60°F
        
        # Humidity effect (humid = less dense, counterintuitively)
        # Water vapor is lighter than dry air
        humidity_factor = (humidity_pct - 50) / 50
        
        # Elevation effect (high = less dense)
        elevation_factor = elevation_ft / 5200  # Normalized to Coors
        
        # Combined (weighted)
        combined = (
            temp_factor * 0.35 +
            humidity_factor * 0.25 +
            elevation_factor * 0.40
        )
        
        return np.clip(combined, -1.5, 1.5)
    
    def analyze_game_conditions(self, game_weather, stadium_name):
        """Analyze specific game conditions"""
        humidity = game_weather.get('humidity_pct', 50)
        temperature = game_weather.get('temperature_c', 20)
        elevation = self.BALLPARK_ELEVATIONS.get(stadium_name, 500)
        
        # Individual factors
        humidity_score = self.calculate_humidity_factor(humidity, temperature)
        elevation_score = self.calculate_elevation_factor(stadium_name)
        
        # Combined air density
        air_density_score = self.calculate_air_density_score(
            humidity, temperature, elevation
        )
        
        # Determine rating
        if air_density_score >= 0.8:
            rating = 'Very Favorable'
        elif air_density_score >= 0.3:
            rating = 'Favorable'
        elif air_density_score >= -0.3:
            rating = 'Neutral'
        elif air_density_score >= -0.8:
            rating = 'Unfavorable'
        else:
            rating = 'Very Unfavorable'
        
        return {
            'humidity_pct': humidity,
            'temperature_c': temperature,
            'elevation_ft': elevation,
            'humidity_score': round(humidity_score, 2),
            'elevation_score': round(elevation_score, 2),
            'air_density_score': round(air_density_score, 2),
            'rating': rating,
            'expected_distance_change_ft': round(air_density_score * 20, 1)  # Est. feet
        }
    
    def analyze_roster(self, roster_df, schedule_df, weather_df):
        """Analyze conditions for all roster players' games"""
        results = []
        
        for _, player in roster_df.iterrows():
            player_name = player['player_name']
            team = player.get('team', 'Unknown')
            
            # Find player's game today
            player_game = schedule_df[
                (schedule_df['home_team'] == team) | 
                (schedule_df['away_team'] == team)
            ]
            
            if len(player_game) == 0:
                continue
            
            game = player_game.iloc[0]
            stadium = game.get('venue', 'Unknown')
            
            # Find weather for this game
            game_weather = weather_df[weather_df['team'] == game['home_team']]
            
            if len(game_weather) == 0:
                game_weather = {'humidity_pct': 50, 'temperature_c': 20}
            else:
                game_weather = game_weather.iloc[0].to_dict()
            
            # Analyze conditions
            analysis = self.analyze_game_conditions(game_weather, stadium)
            
            results.append({
                'player_name': player_name,
                'team': team,
                'stadium': stadium,
                **analysis
            })
        
        return pd.DataFrame(results)


def main():
    """Main execution"""
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / "data"
    
    print("="*80)
    print("Humidity & Elevation Factor Analysis".center(80))
    print("="*80 + "\n")
    
    analyzer = HumidityElevationAnalyzer(data_dir)
    
    # Load data
    roster_files = sorted(data_dir.glob("yahoo_fantasy_rosters_*.csv"),
                         key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not roster_files:
        print("❌ No roster file found!")
        return
    
    roster_df = pd.read_csv(roster_files[0])
    print(f"✓ Loaded roster: {roster_files[0].name} ({len(roster_df)} players)\n")
    
    # Load schedule and weather
    try:
        schedule_2025 = pd.read_csv(data_dir / "mlb_2025_schedule.csv")
        weather_files = sorted(data_dir.glob("weather_data_*.csv"),
                              key=lambda x: x.stat().st_mtime, reverse=True)
        
        if weather_files:
            weather_df = pd.read_csv(weather_files[0])
            print(f"✓ Loaded weather: {weather_files[0].name}\n")
        else:
            print("⚠️  No weather data found - using defaults\n")
            weather_df = pd.DataFrame()
        
        # Analyze
        results_df = analyzer.analyze_roster(roster_df, schedule_2025, weather_df)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = data_dir / f"humidity_elevation_analysis_{timestamp}.csv"
        results_df.to_csv(output_file, index=False)
        
        print(f"✓ Analysis complete: {len(results_df)} players analyzed")
        print(f"📁 Saved to: {output_file.name}\n")
        
        # Summary
        if len(results_df) > 0:
            print("Conditions Summary:")
            print(f"  Very Favorable: {len(results_df[results_df['rating'] == 'Very Favorable'])} games")
            print(f"  Favorable: {len(results_df[results_df['rating'] == 'Favorable'])} games")
            print(f"  Neutral: {len(results_df[results_df['rating'] == 'Neutral'])} games")
            print(f"  Unfavorable: {len(results_df[results_df['rating'] == 'Unfavorable'])} games")
        
    except FileNotFoundError as e:
        print(f"❌ Required data file not found: {e}")
        return
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)


if __name__ == "__main__":
    main()
