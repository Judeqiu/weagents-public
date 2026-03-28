# SKILL.md - CityMap

Generate minimalist city road network maps from OpenStreetMap data.

## What It Does

Renders clean, black-on-white SVG maps of any location worldwide using real OpenStreetMap data. Perfect for wall art, presentations, or urban planning visualization.

**Features:**
- ✅ Fetches real OSM data via Overpass API
- ✅ Geocodes locations with Nominatim
- ✅ Renders clean SVG (no WebGL needed)
- ✅ Multiple road filters (all/basic/strict)
- ✅ Auto-expands tiny bounding boxes
- ✅ Converts to PNG for easy sharing

## Usage

```bash
cd /home/node/.openclaw/workspace/skills/CityMap

# Basic usage
./cityroads "Location Name" -o output.svg

# With options
./cityroads "Singapore City" -o map.svg --width 2000 --roads basic
./cityroads "Tokyo" -o tokyo.svg --roads strict -w 3000
./cityroads "Bukit Panjang" -o bp.svg -w 2000
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | map.svg |
| `-w, --width` | Output width in pixels | 1000 |
| `--roads` | Filter: `all` / `basic` / `strict` | all |
| `--timeout` | API timeout in seconds | 300 (5 min) |

## Road Filters

- `all` — Every highway type (can be very large)
- `basic` — Motorway, primary, secondary, tertiary, residential
- `strict` — Minimal: motorway, primary, secondary only

## Large Cities (Slow Queries)

For large cities, use extended timeout:
```bash
./cityroads "San Jose California" -o sj.svg --timeout 600
./cityroads "Tokyo" -o tokyo.svg -w 3000 --timeout 600
```

## Convert SVG to PNG

```bash
python3 -c "import cairosvg; cairosvg.svg2png(url='map.svg', write_to='map.png', scale=2.0)"
```

## Dependencies

- Python 3.8+
- requests
- (Optional) cairosvg for PNG conversion

## API

Queries Overpass API with filters:
```
way["highway"~"^(motorway|primary|secondary|tertiary|residential)$"]
```

Data is processed into line segments and rendered as SVG polylines.
