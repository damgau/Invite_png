# Project Guidelines: Football Standings Web Scraper

## Overview

Web scraper for Belgian football standings and results that scrapes from **lavenir.net**, transforms HTML data into CSV files, and generates PNG images with team standings and match results. The project follows Clean Architecture with three processing layers.

## Architecture

### Three-Layer Processing Pipeline

1. **Scraper Layer** (`src/scraper.py`)
   - Selenium-based web scraper with headless Chrome
   - Handles navigation, date selection, and page waits
   - Respects rate limiting with configurable `cooldown_seconds` (default: 3s)
   - Returns raw HTML content

2. **Parser Layer** (`src/parse.py`)
   - Extracts structured data from HTML using BeautifulSoup
   - Creates pandas DataFrames for standings and match results
   - Saves CSV files to `data/raw/classements/` and `data/raw/resultats/`
   - Handles team name normalization via `team_renames.json`

3. **Generator Layer** (`src/generate_png.py`)
   - Reads verified CSV files from `data/verified/`
   - Uses Pillow to create PNG images with configured styling
   - Saves output to `data/png/`
   - Loads team abbreviations and colors from JSON config

### Data Flow

```
config.json → Scraper (Selenium) → parse_matches()/parse_classement() 
→ CSV (raw/) → Manual verification → CSV (verified/) → PNG Generator → PNG output
```

## Code Style

- **Type hints**: Not currently used; PRs welcome to add them incrementally
- **Logging**: Use `logging` module; log at INFO level for progress, DEBUG for troubleshooting
- **Naming**: snake_case for functions, UPPER_SNAKE_CASE for constants (e.g., `ELEMENT_WAIT_TIMEOUT`)
- **String formatting**: Use f-strings for config values (see `config.json` loading in `scraper.py`)
- **Path handling**: Use `pathlib.Path` for all file operations (see `scraper.py` line 24-25)

Example from `parse.py`:
```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
logger.info(f"Saving classement to {OUTPUT_FILE}")
```

## Project Conventions

### Configuration Structure

`config.json` defines:
- **Series**: National (D1, D2, D3A) and Provincial (Namur: P1, P2A, P2B, P3C)
- **Titles**: Display names for each series (used in PNG generation)
- **Base URL & paths**: Specific web paths for each series on laverin.net
- **Scraper settings**: `cooldown_seconds` (respect rate limits), `user_agent`

### Team Name Normalization

`team_renames.json` maps scraped team names to standardized team names for consistent CSV/PNG output. Update when scraper encounters new team name variations.

### CSV File Format

**Standings** (`classements/`):
- Columns: position, team_name, matches_played, wins, draws, losses, goals_for, goals_against, points

**Results** (`resultats/`):
- Columns: date_match, time_match, team1, score, team2

Files are processed from `data/raw/` → manually verified → `data/verified/` before PNG generation.

## Build and Test

```bash
# Setup environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run scraper + parser pipeline
python src/main.py         # Scrapes standings and results to data/raw/

# Generate PNG images
python src/generate_png.py # Reads from data/verified/ and outputs to data/png/
```

## Integration Points

### External Dependencies

- **Selenium** (`selenium==4.18.1`): Browser automation with Chrome (headless)
- **BeautifulSoup** (`beautifulsoup4==4.12.2`): HTML parsing
- **Pandas** (`pandas==2.1.4`): DataFrame handling for CSVs
- **Pillow** (`Pillow==10.2.0`): Image generation and text rendering
- **webdriver-manager** (`webdriver-manager==4.0.1`): Automatic ChromeDriver management

### Selenium Waits

- `ELEMENT_WAIT_TIMEOUT = 10`: Finding elements on page
- `PAGE_LOAD_TIMEOUT = 30`: Page load completion
- `DATA_REFRESH_WAIT = 5`: Data refresh after date selection

See `src/scraper.py` lines 30-32 for timeout usage with WebDriverWait.

### Font Paths

PNG generator uses system fonts; currently hardcoded to `/Library/Fonts/entsans.ttf`. May need adjustment on different systems—see `src/generate_png.py` lines 38-48.

## Scraper Politeness

- **Rate limiting**: `cooldown_seconds` enforced between requests (set to 3s by default)
- **User-Agent**: Must be set in `config.json` for identification
- Headless Chrome is used to minimize server load
- No concurrent requests; sequential processing of series
