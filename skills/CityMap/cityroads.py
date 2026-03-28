#!/usr/bin/env python3
"""
City Roads Skill - Generate minimalist road maps from OpenStreetMap data.

Replicates the functionality of anvaka.github.io/city-roads/ but renders
as SVG instead of WebGL for headless environments.
"""

import argparse
import json
import math
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Road query filters (matching city-roads)
ROAD_FILTERS = {
    'all': 'way["highway"]',
    'basic': 'way["highway"~"^(motorway|primary|secondary|tertiary|residential)$"]',
    'strict': 'way["highway"~"^(((motorway|trunk|primary|secondary|tertiary)(_link)?)|unclassified|residential|living_street|pedestrian|service|track)$"][area!="yes"]',
}


def geocode_location(name):
    """Use Nominatim to find location bounding box."""
    query_params = urllib.parse.urlencode({
        'q': name,
        'format': 'json',
        'limit': 1,
        'polygon_geojson': 0
    })
    
    url = f"{NOMINATIM_URL}?{query_params}"
    headers = {'User-Agent': 'CityRoadsSkill/1.0'}
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            if not data:
                return None
            
            place = data[0]
            # boundingbox is [min_lat, max_lat, min_lon, max_lon]
            bb = place.get('boundingbox', [])
            if len(bb) >= 4:
                min_lat, max_lat, min_lon, max_lon = float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3])
                
                # Check if bounding box is too small (less than ~500m)
                lat_diff = max_lat - min_lat
                lon_diff = max_lon - min_lon
                
                # Expand tiny bounding boxes to at least ~2km
                min_size = 0.02  # roughly 2km
                if lat_diff < min_size:
                    center_lat = (min_lat + max_lat) / 2
                    min_lat = center_lat - min_size / 2
                    max_lat = center_lat + min_size / 2
                if lon_diff < min_size:
                    center_lon = (min_lon + max_lon) / 2
                    min_lon = center_lon - min_size / 2
                    max_lon = center_lon + min_size / 2
                
                return {
                    'name': place.get('display_name', name),
                    'lat': float(place.get('lat', 0)),
                    'lon': float(place.get('lon', 0)),
                    'bbox': [min_lon, min_lat, max_lon, max_lat]
                }
    except Exception as e:
        print(f"Geocoding error: {e}", file=sys.stderr)
    
    return None


def fetch_roads(bbox, road_filter='basic', timeout=300):
    """Fetch road data from Overpass API."""
    min_lon, min_lat, max_lon, max_lat = bbox
    
    # Build Overpass query with generous timeout
    query = f"""[out:json][timeout:{timeout}];
({road_filter}({min_lat},{min_lon},{max_lat},{max_lon});
);
(._;>;);
out body;"""
    
    print(f"Fetching roads... (this may take a while, timeout: {timeout}s)", file=sys.stderr)
    
    req = urllib.request.Request(
        OVERPASS_URL,
        data=query.encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    
    try:
        # Use 60s connection timeout, but let Overpass take its time (up to 300s)
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Overpass API error: {e.code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching roads: {e}", file=sys.stderr)
        return None


def process_osm_data(data):
    """Process OSM response into nodes and ways."""
    nodes = {}
    ways = []
    
    for element in data.get('elements', []):
        if element['type'] == 'node':
            nodes[element['id']] = (element['lon'], element['lat'])
        elif element['type'] == 'way':
            ways.append(element.get('nodes', []))
    
    return nodes, ways


def mercator_projection(lon, lat, center_lon, center_lat):
    """Mercator projection (same as city-roads uses)."""
    # Earth radius in meters
    R = 6371393
    
    # Convert to radians
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)
    center_lon_rad = math.radians(center_lon)
    center_lat_rad = math.radians(center_lat)
    
    # Mercator projection
    x = R * (lon_rad - center_lon_rad)
    y = R * (math.log(math.tan(math.pi/4 + lat_rad/2)) - 
             math.log(math.tan(math.pi/4 + center_lat_rad/2)))
    
    return x, -y  # Flip Y to match SVG coordinates


def render_svg(nodes, ways, width=800, height=800, title=""):
    """Render roads as SVG."""
    if not nodes or not ways:
        return None
    
    # Calculate bounds
    lons = [n[0] for n in nodes.values()]
    lats = [n[1] for n in nodes.values()]
    
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # Project all nodes
    projected = {}
    for node_id, (lon, lat) in nodes.items():
        projected[node_id] = mercator_projection(lon, lat, center_lon, center_lat)
    
    # Calculate projected bounds
    xs = [p[0] for p in projected.values()]
    ys = [p[1] for p in projected.values()]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Scale to fit SVG
    padding = 20
    available_width = width - 2 * padding
    available_height = height - 2 * padding
    
    data_width = max_x - min_x
    data_height = max_y - min_y
    
    if data_width == 0 or data_height == 0:
        return None
    
    scale_x = available_width / data_width
    scale_y = available_height / data_height
    scale = min(scale_x, scale_y)
    
    # Center the data
    offset_x = padding + (available_width - data_width * scale) / 2 - min_x * scale
    offset_y = padding + (available_height - data_height * scale) / 2 - min_y * scale
    
    def to_svg_coords(x, y):
        return x * scale + offset_x, y * scale + offset_y
    
    # Generate SVG lines
    svg_lines = []
    for way in ways:
        points = []
        for node_id in way:
            if node_id in projected:
                x, y = projected[node_id]
                sx, sy = to_svg_coords(x, y)
                points.append(f"{sx:.2f},{sy:.2f}")
        
        if len(points) > 1:
            svg_lines.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#1a1a1a" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>')
    
    # Build SVG
    title_element = f'<text x="{width-20}" y="{height-20}" text-anchor="end" font-family="sans-serif" font-size="14" fill="#666">{title}</text>' if title else ''
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<rect width="{width}" height="{height}" fill="#fafafa"/>
<g id="roads">
{chr(10).join(svg_lines)}
</g>
{title_element}
</svg>'''
    
    return svg


def main():
    parser = argparse.ArgumentParser(description='Generate minimalist road maps from OpenStreetMap')
    parser.add_argument('location', help='City or location name')
    parser.add_argument('-o', '--output', help='Output file path', default=None)
    parser.add_argument('-w', '--width', type=int, default=800, help='Output width in pixels')
    parser.add_argument('-H', '--height', type=int, default=800, help='Output height in pixels')
    parser.add_argument('--roads', choices=['all', 'basic', 'strict'], default='basic',
                        help='Road filter type')
    parser.add_argument('--timeout', type=int, default=300, help='API timeout in seconds (default: 300s for large cities)')
    
    args = parser.parse_args()
    
    # Step 1: Geocode location
    print(f"Looking up: {args.location}", file=sys.stderr)
    location = geocode_location(args.location)
    
    if not location:
        print(f"Could not find location: {args.location}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found: {location['name']}", file=sys.stderr)
    print(f"Bounds: {location['bbox']}", file=sys.stderr)
    
    # Step 2: Fetch road data
    road_filter = ROAD_FILTERS[args.roads]
    data = fetch_roads(location['bbox'], road_filter, args.timeout)
    
    if not data:
        print("Failed to fetch road data", file=sys.stderr)
        sys.exit(1)
    
    # Step 3: Process data
    nodes, ways = process_osm_data(data)
    print(f"Got {len(nodes)} nodes, {len(ways)} ways", file=sys.stderr)
    
    if not ways:
        print("No roads found in this area", file=sys.stderr)
        sys.exit(1)
    
    # Step 4: Render SVG
    svg = render_svg(nodes, ways, args.width, args.height, args.location)
    
    if not svg:
        print("Failed to render SVG", file=sys.stderr)
        sys.exit(1)
    
    # Step 5: Output
    if args.output:
        Path(args.output).write_text(svg)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(svg)


if __name__ == '__main__':
    import urllib.parse  # noqa
    main()
