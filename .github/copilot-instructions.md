# Project Guidelines: PNG Event Generator

## Overview

Python script that automatically generates 3 PNG images per event from CSV data:
1. **Name PNG** (`prenom.png`) - Name in pink frame
2. **Theme PNG** (`prenom_thema.png`) - Background with event description
3. **Info PNG** (`prenom_QQO.png`) - Complete event details (What/When/Where/Contact)

## Architecture

### Single-Layer Processing

1. **CSV Parser** (`png_generator.py`)
   - Reads tab-separated CSV ([`data.csv`](data.csv))
   - Processes each row to extract event data
   - Validates required fields (7 columns minimum)

2. **PNG Generator** (`png_generator.py`)
   - Uses Pillow for image creation (1920x1080 RGBA)
   - Applies custom fonts, colors, and text effects
   - Saves output to `export_png/`

### Data Flow

```
data.csv → CSV Parser → PNG Generator (Pillow) → export_png/*.png
```

## Code Style

- **Type hints**: Not currently used
- **Encoding**: UTF-8 with `# -*- coding: utf-8 -*-`
- **Naming**: snake_case for functions, UPPER_SNAKE_CASE for constants
- **String formatting**: Use f-strings for all string interpolation
- **Path handling**: Use `pathlib.Path` for all file operations (cross-platform compatibility)
- **Comments**: French comments and docstrings (user-facing)

Example from [`png_generator.py`](png_generator.py):
```python
SCRIPT_DIR = Path(__file__).resolve().parent
CSV_FILE = SCRIPT_DIR / "data.csv"
OUTPUT_DIR = SCRIPT_DIR / "export_png"
```

## Project Conventions

### CSV File Format

Tab-separated values (TSV) with 7 columns:

```
QUOI    QUAND    OÙ    NOM    HEURE    DATE_SOURCE    CONTACT
```

- **Pipe delimiter (`|`)**: Forces line break in multi-line text
- **Encoding**: UTF-8 (required for French accents)
- **Separator**: Tab character (`\t`) or comma (auto-detected)

See [`data.csv`](data.csv) for examples.

### Font Configuration

- **Name PNG**: [`icecream-standard.otf`](icecream-standard.otf) at 70px (66% scale)
- **Theme/Info PNG**: [`ligurino bold.ttf`](ligurino bold.ttf) at 57px/77px
- Fonts must be at project root

### Image Specifications

**Dimensions**: 1920x1080 RGBA  
**Background**: [`invite.png`](invite.png) (transparent, 1920x1080)  
**Colors**:
- White text: RGB(251, 251, 251, 255)
- Pink frame: RGB(255, 116, 162, 243)

**Text Effects** (Info PNG):
- Drop shadow: 90% opacity, 84° angle, 2px distance, 5px blur

### Output Files

For each CSV row with name "John Doe":
- `John_Doe.png` - Name in pink frame
- `John_Doe_thema.png` - Event theme with background
- `John_Doe_QQO.png` - Full event details

## Build and Test

```bash
# Quick start (Windows)
run_windows.bat

# Quick start (macOS/Linux)
./run_mac.sh

# Manual setup
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
python png_generator.py
```

## Integration Points

### External Dependencies

- **Pillow** (`Pillow==10.2.0`): Image generation, fonts, effects

### Launcher Scripts

- **Windows**: [`run_windows.bat`](run_windows.bat) - Auto-setup with venv
- **macOS/Linux**: [`run_mac.sh`](run_mac.sh) - Auto-setup with venv

Both scripts handle:
1. Python installation check
2. Virtual environment creation
3. Dependency installation
4. PNG generation
5. Opening output folder

### Font Loading

Fonts are loaded with absolute paths via `pathlib.Path`:

```python
FONT_ICE_CREAM = SCRIPT_DIR / "icecream-standard.otf"
font = ImageFont.truetype(str(FONT_ICE_CREAM), FONT_SIZE_PNG1)
```

## User-Facing Messages

All error messages and prompts are in **French**:
- "⚠ Erreur : Python n'est pas installé"
- "✓ Créé : export_png/John_Doe.png"
- "✅ Terminé ! 6 PNG générés"

Keep this convention for consistency with [`README.md`](README.md).