# Fantasy Baseball AI - System Architecture

## Overview

Fantasy Baseball AI is a comprehensive sit/start recommendation system that analyzes 20+ factors to provide data-driven lineup decisions. The system combines machine learning, statistical analysis, and real-time data from multiple sources.

## High-Level Architecture

```mermaid
graph TB
    subgraph "External Data Sources"
        MLB[MLB Stats API]
        Yahoo[Yahoo Fantasy API]
        Weather[Weather API]
        Vegas[Vegas Odds API]
        Statcast[MLB Statcast]
    end
    
    subgraph "Data Collection Layer"
        Scrapers[Data Scrapers]
        MLB --> Scrapers
        Yahoo --> Scrapers
        Weather --> Scrapers
        Vegas --> Scrapers
        Statcast --> Scrapers
    end
    
    subgraph "Storage Layer"
        RawData[(Raw Data CSVs)]
        Scrapers --> RawData
    end
    
    subgraph "Factor Analysis Engine"
        FA[20 Factor Analyzers]
        RawData --> FA
    end
    
    subgraph "ML & Optimization"
        Weights[Weight Optimization]
        XGB[XGBoost Model]
        FA --> Weights
        FA --> XGB
    end
    
    subgraph "Scoring Engine"
        Scorer[Final Score Calculator]
        Weights --> Scorer
        XGB --> Scorer
    end
    
    subgraph "Presentation Layer"
        Dashboard[Streamlit Dashboard]
        Scorer --> Dashboard
    end
    
    User[Fantasy Manager] --> Dashboard
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Dashboard
    participant Scorer
    participant FA as Factor Analyzers
    participant Data as Data Layer
    participant External as External APIs
    
    User->>Dashboard: Request sit/start for date
    Dashboard->>Data: Load roster
    Data->>External: Fetch latest data
    External-->>Data: Return game data, odds, weather
    Data-->>Dashboard: Roster players
    
    loop For each player
        Dashboard->>FA: Analyze player
        FA->>Data: Get historical stats
        FA->>Data: Get matchup info
        FA->>Data: Get park factors
        FA-->>Dashboard: Factor scores
    end
    
    Dashboard->>Scorer: Calculate final scores
    Scorer->>Scorer: Apply weights
    Scorer-->>Dashboard: Final recommendations
    Dashboard-->>User: Display sit/start analysis
```

## Factor Analysis System

```mermaid
graph LR
    subgraph "High Impact 10-20%"
        Vegas[Vegas Odds<br/>15-20%]
        Statcast[Statcast Metrics<br/>10-15%]
    end
    
    subgraph "Medium-High 8-12%"
        Matchup[Matchup History<br/>8-12%]
        Bullpen[Bullpen Fatigue<br/>8-12%]
        Platoon[Platoon Splits<br/>8-12%]
    end
    
    subgraph "Medium 5-8%"
        HomeAway[Home/Away<br/>5-8%]
        Injury[Injury Status<br/>5-8%]
        Park[Park Factors<br/>5-8%]
        Form[Recent Form<br/>5-8%]
        Wind[Wind<br/>5-8%]
    end
    
    subgraph "Lower 3-5%"
        Rest[Rest Days<br/>3-5%]
        Temp[Temperature<br/>3-5%]
        Lineup[Lineup Position<br/>3-5%]
        Umpire[Umpire<br/>3-5%]
        PitchMix[Pitch Mix<br/>3-5%]
    end
    
    subgraph "Minimal 1-3%"
        Time[Time of Day<br/>1-3%]
        Humidity[Humidity<br/>1-3%]
        Defense[Defense<br/>1-3%]
        Monthly[Monthly Splits<br/>1-3%]
        Momentum[Momentum<br/>1-3%]
    end
    
    Vegas --> Scorer[Weighted Score<br/>Calculator]
    Statcast --> Scorer
    Matchup --> Scorer
    Bullpen --> Scorer
    Platoon --> Scorer
    HomeAway --> Scorer
    Injury --> Scorer
    Park --> Scorer
    Form --> Scorer
    Wind --> Scorer
    Rest --> Scorer
    Temp --> Scorer
    Lineup --> Scorer
    Umpire --> Scorer
    PitchMix --> Scorer
    Time --> Scorer
    Humidity --> Scorer
    Defense --> Scorer
    Monthly --> Scorer
    Momentum --> Scorer
    
    Scorer --> Final[Final Score<br/>-2 to +2]
```

## Weight Optimization Process

```mermaid
flowchart TD
    Start[Start Weight Tuning] --> LoadData[Load Historical Data]
    LoadData --> InitWeights[Initialize Random Weights]
    
    InitWeights --> Trial{Trial N}
    Trial --> CalcScores[Calculate Scores<br/>with Current Weights]
    CalcScores --> Backtest[Backtest Against<br/>Actual Results]
    Backtest --> Metric[Calculate Performance<br/>Metric]
    
    Metric --> Compare{Better than<br/>Best?}
    Compare -->|Yes| UpdateBest[Update Best Weights]
    Compare -->|No| AdjustWeights[Adjust Weights]
    UpdateBest --> AdjustWeights
    
    AdjustWeights --> MoreTrials{More Trials?}
    MoreTrials -->|Yes| Trial
    MoreTrials -->|No| SaveWeights[Save Optimized Weights]
    
    SaveWeights --> End[End]
```

## XGBoost ML Pipeline

```mermaid
flowchart LR
    subgraph "Feature Engineering"
        FactorScores[Factor Scores<br/>20 features]
        Historical[Historical Performance<br/>7/14/30 day stats]
        Context[Contextual Features<br/>Home/Away, Platoon]
    end
    
    subgraph "Training Data"
        FactorScores --> Features[Feature Matrix]
        Historical --> Features
        Context --> Features
        ActualResults[Actual Game Results] --> Target[Target Variable<br/>Fantasy Points]
    end
    
    subgraph "XGBoost Model"
        Features --> Train[Train XGBoost]
        Target --> Train
        Train --> Model[Trained Model]
    end
    
    subgraph "Prediction"
        NewPlayer[New Player Data] --> Model
        Model --> Prediction[Predicted Points]
    end
    
    Prediction --> Combine[Combine with<br/>Factor Weights]
    Combine --> FinalScore[Final Recommendation]
```

## Daily Analysis Workflow

```mermaid
sequenceDiagram
    participant Cron as Scheduler
    participant Script as daily_sitstart.py
    participant Scraper as Data Scrapers
    participant FA as Factor Analyzers
    participant Weights as Weight Engine
    participant Output as CSV Output
    
    Cron->>Script: Trigger daily run (8am)
    
    Script->>Scraper: Fetch Yahoo roster
    Scraper-->>Script: Player list
    
    Script->>Scraper: Fetch MLB game logs
    Scraper-->>Script: Recent performance
    
    Script->>Scraper: Fetch today's matchups
    Scraper-->>Script: Opponent info
    
    Script->>Scraper: Fetch weather/vegas data
    Scraper-->>Script: External data
    
    loop For each player
        Script->>FA: Run 20 factor analyses
        FA-->>Script: Factor scores
    end
    
    Script->>Weights: Apply optimized weights
    Weights-->>Script: Weighted scores
    
    Script->>Output: Generate recommendations
    Output-->>Script: CSV saved
    
    Script->>Script: Trigger Streamlit update
```

## Streamlit Dashboard Architecture

```mermaid
graph TB
    subgraph "Main Entry Point"
        Main[streamlit_report.py]
    end
    
    subgraph "Component Modules"
        Config[config.py<br/>Page Setup, CSS]
        DataLoader[data_loaders.py<br/>Load CSVs, Cache Data]
        Summary[summary_metrics.py<br/>Summary Stats]
        Roster[current_roster_performance.py<br/>7/14/30 Day Stats]
        TopSits[top_starts_sits.py<br/>Recommendations]
        Weights[player_weight_breakdown.py<br/>Factor Weights]
        FactorViz[factor_analysis.py<br/>Visualizations]
        Rankings[full_rankings.py<br/>Complete Table]
        Waiver[waiver_wire.py<br/>FA Prospects]
        Legend[legend.py<br/>Help & Docs]
    end
    
    subgraph "Data Sources"
        RecCSV[(sitstart_recommendations_*.csv)]
        RosterCSV[(yahoo_fantasy_rosters_*.csv)]
        GameLogs[(mlb_game_logs_*.csv)]
        WaiverCSV[(waiver_wire_*.csv)]
    end
    
    Main --> Config
    Main --> DataLoader
    DataLoader --> RecCSV
    DataLoader --> RosterCSV
    DataLoader --> GameLogs
    DataLoader --> WaiverCSV
    
    Main --> Summary
    Main --> Roster
    Main --> TopSits
    Main --> Weights
    Main --> FactorViz
    Main --> Rankings
    Main --> Waiver
    Main --> Legend
```

## Data Storage Schema

```mermaid
erDiagram
    ROSTER {
        string player_name
        string position
        string mlb_team
        string fantasy_team
        string player_key
    }
    
    GAME_LOGS {
        int player_id
        date game_date
        int game_pk
        boolean is_home
        boolean is_win
        string opponent
        int AB
        int H
        int R
        int RBI
        int HR
        float AVG
        float OPS
    }
    
    RECOMMENDATIONS {
        string player_name
        date analysis_date
        float final_score
        string recommendation
        float vegas_score
        float statcast_score
        float matchup_score
        string ellipsis "..."
        float momentum_score
        float vegas_weight
        float statcast_weight
        string ellipsis2 "..."
        float momentum_weight
    }
    
    WAIVER_WIRE {
        string player_name
        string position
        string mlb_team
        float final_score
        string recommendation
        boolean is_available
    }
    
    MLB_PLAYERS {
        int player_id
        string player_name
        string position
        string position_type
        string mlb_team
    }
    
    ROSTER ||--o{ GAME_LOGS : "has stats"
    ROSTER ||--o{ RECOMMENDATIONS : "gets analysis"
    MLB_PLAYERS ||--o{ GAME_LOGS : "records"
    WAIVER_WIRE ||--o{ RECOMMENDATIONS : "similar to"
```

## External API Integration

```mermaid
graph TB
    subgraph "MLB Stats API"
        MLBGames[Game Schedule]
        MLBStats[Player Stats]
        MLBPlayers[Player Info]
    end
    
    subgraph "Yahoo Fantasy API"
        YahooAuth[OAuth 2.0 Auth]
        YahooRoster[Roster Data]
        YahooLeague[League Settings]
    end
    
    subgraph "Weather API"
        WeatherCurrent[Current Conditions]
        WeatherForecast[Game Time Forecast]
    end
    
    subgraph "Vegas Odds API"
        VegasLines[Betting Lines]
        VegasOU[Over/Under]
        VegasProb[Win Probability]
    end
    
    subgraph "MLB Statcast"
        StatcastBatting[Exit Velocity]
        StatcastPitching[Spin Rate]
        StatcastMetrics[xBA, xSLG]
    end
    
    subgraph "Our System"
        Scrapers[Data Scrapers]
        Cache[(Local Cache)]
    end
    
    YahooAuth --> YahooRoster
    YahooAuth --> YahooLeague
    
    MLBGames --> Scrapers
    MLBStats --> Scrapers
    MLBPlayers --> Scrapers
    YahooRoster --> Scrapers
    WeatherCurrent --> Scrapers
    WeatherForecast --> Scrapers
    VegasLines --> Scrapers
    VegasOU --> Scrapers
    VegasProb --> Scrapers
    StatcastBatting --> Scrapers
    StatcastPitching --> Scrapers
    StatcastMetrics --> Scrapers
    
    Scrapers --> Cache
```

## Scoring Algorithm

```mermaid
flowchart TD
    Start[Player + Date] --> LoadFactors[Load Factor Scores<br/>20 factors]
    LoadFactors --> LoadWeights[Load Optimized Weights<br/>Player-specific]
    
    LoadWeights --> Multiply[Multiply Each Factor<br/>Score × Weight]
    
    Multiply --> Sum[Sum All Weighted Scores]
    
    Sum --> Normalize[Normalize to -2 to +2 range]
    
    Normalize --> Classify{Classify Score}
    
    Classify -->|>= 0.15| StrongStart[🌟 Strong Start]
    Classify -->|>= 0.05| Favorable[✅ Favorable]
    Classify -->|-0.05 to 0.05| Neutral[⚖️ Neutral]
    Classify -->|>= -0.15| Unfavorable[⚠️ Unfavorable]
    Classify -->|< -0.15| Bench[🚫 Bench]
    
    StrongStart --> Output[Generate Recommendation]
    Favorable --> Output
    Neutral --> Output
    Unfavorable --> Output
    Bench --> Output
```

## Key Technologies

- **Language**: Python 3.12
- **ML Framework**: XGBoost, scikit-learn
- **Dashboard**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: plotly
- **APIs**: Yahoo Fantasy, MLB Stats API
- **Storage**: CSV files (local filesystem)
- **Caching**: Streamlit @st.cache_data
- **Scheduling**: cron / manual execution

## Performance Characteristics

- **Analysis Time**: 30-120 seconds per date
- **Players Analyzed**: ~25-60 per roster
- **Factors Calculated**: 20 per player
- **Historical Data**: Last 3 years (optional)
- **Cache Duration**: Session-based
- **Update Frequency**: Daily (morning)

## System Requirements

- Python 3.12+
- 4GB RAM minimum
- 1GB disk space for historical data
- Internet connection for API access
- Yahoo Fantasy API credentials

## Future Architecture Enhancements

1. **Database Migration**: Move from CSV to PostgreSQL/SQLite
2. **Real-time Updates**: WebSocket integration for live updates
3. **API Layer**: REST API for mobile app integration
4. **Containerization**: Docker for easier deployment
5. **CI/CD**: Automated testing and deployment
6. **Caching Layer**: Redis for improved performance
7. **Message Queue**: Celery for async processing
