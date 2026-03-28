# City Roads Skill

Generate minimalist road network maps from OpenStreetMap data.

## Overview

This skill fetches road data from OpenStreetMap via the Overpass API and renders it as clean, minimalist black-on-white SVG maps — similar to the city-roads project but without requiring WebGL.

## Usage

```bash
./cityroads singapore              # Generate map for Singapore
./cityroads "New York" --output nyc.svg
./cityroads tokyo --width 1200     # Custom width
./cityroads london --roads basic   # Use basic road filter
```

## Features

- Fetches real OpenStreetMap data
- Renders as clean SVG (no WebGL required)
- Supports multiple road filters (all, basic, strict)
- Configurable output size
- Works in headless environments

## Road Filters

- `all` - Every highway type (can be very large)
- `basic` - Motorway, primary, secondary, tertiary, residential
- `strict` - Same as city-roads strict filter

## Dependencies

- Python 3.8+
- requests
- (Optional) osmnx for advanced queries

## API

The skill queries Overpass API with filters like:
```
way["highway"~"^(motorway|primary|secondary|tertiary|residential)$"]
```

Data is processed into line segments and rendered as SVG polylines.
