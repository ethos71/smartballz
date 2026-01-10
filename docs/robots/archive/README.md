# Archive

This folder contains old versions of files, deprecated code, and historical documentation preserved for reference.

## Purpose

All archived and deprecated code should be moved here to keep the main codebase clean while preserving historical context.

## Organization Rules

When archiving files:
1. Include the original filename
2. Update this README with archive details
3. Note the date archived
4. Document why it was archived
5. Reference any replacement code/files

## Contents

### streamlit_report_original.py
- **Date Archived:** 2025-11-16
- **Size:** 2,157 lines (monolithic version)
- **Reason:** Replaced with modular v2 (now streamlit_report.py)
- **Description:** Original single-file Streamlit dashboard before modularization

## Modularization Details

The original monolithic file was split into 8 reusable components:

**New Structure:**
```
streamlit_report.py (265 lines - main orchestration)
├── src/scripts/streamlit_components/
    ├── summary_metrics.py (~90 lines)
    ├── current_roster_performance.py (~240 lines)
    ├── top_starts_sits.py (~170 lines)
    ├── player_weight_breakdown.py (~220 lines)
    ├── factor_analysis.py (~130 lines)
    ├── full_rankings.py (~175 lines)
    ├── waiver_wire_section.py (~200 lines)
    └── data_loaders.py (~180 lines)
```

**Benefits:**
- 89% smaller main file (2,157 → 265 lines)
- Reusable components
- Better maintainability
- Easier testing
- Clear separation of concerns

**Commits:**
- 179654d: Initial component extraction
- 455527d: Additional components
- 0e8e8fb: Complete v2 implementation
- 1dc90b6: Final fixes and original chart restoration
- Made permanent: 2025-11-16
