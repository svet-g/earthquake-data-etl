# Earthquake Data ETL Pipeline

A Python ETL pipeline that extracts earthquake data from USGS, transforms it for analysis, and loads it into PostgreSQL.

## What it does

- **Extract**: Pulls earthquake data from USGS API (last 30 days)
- **Transform**: Filters for accurate earthquake events, converts coordinates, creates depth categories
- **Load**: Stores processed data in PostgreSQL with data quality constraints

## Requirements

- Python >=3.6
- PostgreSQL database
- Dependencies in `requirements.txt`

## Setup

1. **Install the package**:
   ```bash
   pip install -e .
   ```

2. **Create environment files**:
   - `.env` (for prod)
   - `.env.test` (for test)
   - `.env.dev` (for dev)
   
   With database configuration:
   ```
   SOURCE_DB_NAME=your_source_db
   SOURCE_DB_USER=your_user
   SOURCE_DB_PASSWORD=your_password
   SOURCE_DB_HOST=your_host
   SOURCE_DB_PORT=5432
   
   TARGET_DB_NAME=your_target_db
   TARGET_DB_USER=your_user
   TARGET_DB_PASSWORD=your_password
   TARGET_DB_HOST=your_host
   TARGET_DB_PORT=5432
   ```

## Usage

**Run ETL Pipeline**:
```bash
run_etl prod    # Production environment
run_etl dev     # Development environment  
run_etl test    # Test environment
```

**Run Tests**:
```bash
run_tests unit         # Unit tests only
run_tests component    # Component tests only
run_tests integration  # Integration tests only
run_tests all          # All tests
run_tests lint         # Lint checks (flake8, sqlfluff)
```

## Data Transformations

- Filters events where `type == 'earthquake'` and `gap < 180` (for location accuracy)
- Converts GeoJSON geometry to separate latitude, longitude, depth columns
- Creates depth categories: shallow (<60km), intermediate (60-300km), deep (300-700km), highest_depth (>700km)
- Converts Unix timestamps to datetime
- Drops unnecessary columns for cleaner dataset

## Project Structure

```
├── config/          # Database and environment configuration
├── data/            # Raw, processed, and test data
├── notebooks/       # EDA analysis
├── scripts/         # Main ETL runner
├── src/             # ETL modules (extract, transform, load, utils)
├── tests/           # Unit, component, and integration tests
└── pyproject.toml   # Package configuration
```

## Output

Creates `earthquakes-svet-g` table in PostgreSQL with:
- Primary key constraint on `id`
- Latitude/longitude range validation
- Significance value validation

---

**Author**: Svetlana Gljadelkina  
**License**: MIT
