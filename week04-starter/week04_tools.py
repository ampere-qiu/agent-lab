"""Classroom cargo estimate and local report/map output. No LLM calls here."""
import html
import json
import math
from pathlib import Path
from smolagents import tool

OUTPUT = Path(__file__).resolve().parent / "outputs"


@tool
def cargo_time(latitude: float, longitude: float) -> float:
    """Estimate cargo flight hours from fictional Gotham (New York coordinates).
    Args:
        latitude: Destination latitude in degrees, from -90 to 90.
        longitude: Destination longitude in degrees, from -180 to 180.
    """
    if not math.isfinite(latitude) or not math.isfinite(longitude):
        raise ValueError("Coordinates must be finite")
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("Coordinates out of range")
    a, b, c, d = map(math.radians, [40.7128, -74.0060, latitude, longitude])
    h = math.sin((c-a)/2)**2 + math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    km = 6371 * 2 * math.asin(math.sqrt(min(1.0, max(0.0, h))))
    return round(km * 1.1 / 750 + 1, 2)


@tool
def save_report(rows_json: str) -> str:
    """Save a sourced table and colored coordinate map in outputs/batman-report.html.
    Args:
        rows_json: JSON list of objects with location, kind, latitude, longitude, source_url, coordinate_source_url, and evidence fields. kind is filming or factory.
    """
    rows = json.loads(rows_json)
    if not isinstance(rows, list) or not rows:
        raise ValueError("Supply a nonempty list of rows")
    table, dots = [], []
    for row in rows:
        lat, lon = float(row["latitude"]), float(row["longitude"])
        hours = cargo_time(lat, lon)
        sources = []
        for key in ("source_url", "coordinate_source_url"):
            url = str(row[key])
            if not url.startswith("https://"):
                raise ValueError("Source URLs must start with https://")
            sources.append(html.escape(url, quote=True))
        name, evidence, kind = (html.escape(str(row[k])) for k in ("location", "evidence", "kind"))
        table.append(f'<tr><td>{name}</td><td>{kind}</td><td>{lat}, {lon}</td><td>{hours}</td>'
                     f'<td><a href="{sources[0]}">location evidence</a>; '
                     f'<a href="{sources[1]}">coordinates</a></td><td>{evidence}</td></tr>')
        color = "#7c3aed" if hours < 5 else "#dc2626"
        dots.append(f'<circle cx="{(lon+180)*2}" cy="{(90-lat)*2}" r="5" fill="{color}"><title>{name}: {hours} h</title></circle>')
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "batman-report.html"
    destination.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Batman research report</title>'
        '<style>body{font:16px system-ui;margin:2rem}td,th{padding:.5rem;border:1px solid #ccc}table{border-collapse:collapse}svg{max-width:100%;background:#eef2ff}</style>'
        '<h1>Batman research report</h1><p>Classroom estimate: 750 km/h, 10% distance allowance, plus 1 hour. Not a transport schedule.</p>'
        '<table><tr><th>Location</th><th>Kind</th><th>Latitude, longitude</th><th>Hours</th><th>Sources</th><th>Evidence / uncertainty</th></tr>'
        + ''.join(table) + '</table><h2>Coordinate map</h2><p>Equirectangular longitude/latitude plot; no geographic basemap. Purple: under 5 hours; red: 5 hours or more.</p>'
        '<svg viewBox="0 0 720 360" role="img" aria-label="Location coordinate map">'
        '<path d="M0 180H720 M360 0V360" stroke="#999"/>' + ''.join(dots) + '</svg></html>', encoding="utf-8")
    return str(destination)
