import re

COMPONENT_KEYWORDS = {
    'column': 'Column',
    'distillation column': 'Column',
    'tray column': 'Column',
    'pump': 'Pump',
    'reactor': 'Reactor',
    'cstr': 'Reactor',
    'pfr': 'Reactor',
    'reboiler': 'Reboiler',
    'condenser': 'Condenser',
    'cooler': 'Condenser',
    'heat exchanger': 'Condenser',
    'tank': 'Tank',
    'feed tank': 'Tank',
    'separator': 'Separator',
}

ORDER_PREFERENCE = ['Tank', 'Pump', 'Column', 'Reactor', 'Reboiler', 'Condenser', 'Separator']

SVG_HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
.text {{ font-family: Arial, sans-serif; font-size: 12px; }}
.comp {{ fill: #fff; stroke: #222; stroke-width: 2 }}
.conn {{ stroke: #222; stroke-width: 2; fill: none; marker-end: url(#arrow) }}
</style>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L10,5 L0,10 z" />
</marker>
</defs>
'''

SVG_FOOTER = '</svg>\n'

def extract_components(text):
    text_low = text.lower()
    found = []
    for kw, name in COMPONENT_KEYWORDS.items():
        if kw in text_low:
            count = len(re.findall(re.escape(kw), text_low))
            for _ in range(count):
                found.append(name)
    comps = []
    counts = {}
    for c in found:
        counts[c] = counts.get(c, 0) + 1
    for c, n in counts.items():
        for i in range(n):
            comps.append(c)
    return comps

def layout_components(comps, width=1000, height=400):
    columns = {k: [] for k in ORDER_PREFERENCE}
    others = []
    for c in comps:
        if c in columns:
            columns[c].append(c)
        else:
            others.append(c)
    ordered = []
    for k in ORDER_PREFERENCE:
        ordered += columns[k]
    ordered += others
    n = max(1, len(ordered))
    margin = 80
    usable_w = width - 2*margin
    spacing = usable_w / max(1, n-1) if n>1 else 0
    positions = []
    for i, comp in enumerate(ordered):
        x = margin + i * spacing
        y = height / 2
        positions.append({'type': comp, 'x': x, 'y': y})
    return positions

def draw_component(svg_parts, comp):
    x = comp['x']; y = comp['y']; t = comp['type']
    w = 120; h = 70
    rx = 8
    left = x - w/2; top = y - h/2
    if t == 'Column':
        h2 = 140
        top = y - h2/2
        svg_parts.append(f'<rect class="comp" x="{x-40}" y="{top}" width="80" height="{h2}" rx="12" />')
        svg_parts.append(f'<text class="text" x="{x}" y="{top + h2 + 16}" text-anchor="middle">{t}</text>')
    elif t in ('Reactor', 'Tank', 'Separator'):
        svg_parts.append(f'<ellipse class="comp" cx="{x}" cy="{y}" rx="48" ry="36" />')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + 52}" text-anchor="middle">{t}</text>')
    elif t in ('Pump',):
        points = f"{x},{y-28} {x+28},{y} {x},{y+28} {x-28},{y}"
        svg_parts.append(f'<polygon class="comp" points="{points}" />')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + 42}" text-anchor="middle">{t}</text>')
    elif t in ('Reboiler','Condenser'):
        svg_parts.append(f'<rect class="comp" x="{left}" y="{top}" width="{w}" height="{h}" rx="{rx}" />')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + h/2 + 8}" text-anchor="middle">{t}</text>')
    else:
        svg_parts.append(f'<rect class="comp" x="{left}" y="{top}" width="{w}" height="{h}" rx="{rx}" />')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + h/2 + 8}" text-anchor="middle">{t}</text>')

def connect(svg_parts, compA, compB):
    x1,y1 = compA['x'], compA['y']
    x2,y2 = compB['x'], compB['y']
    path = f"M{x1},{y1} L{(x1+x2)/2},{y1} L{(x1+x2)/2},{y2} L{x2},{y2}"
    svg_parts.append(f'<path class="conn" d="{path}" />')

def text_to_svg(description, outfile='pfd.svg'):
    comps = extract_components(description)
    if not comps:
        print("No components detected from description.")
        return
    positions = layout_components(comps)
    width = 1000; height = 500
    svg_parts = [SVG_HEADER.format(w=width, h=height)]
    for p in positions:
        draw_component(svg_parts, p)
    for i in range(len(positions)-1):
        connect(svg_parts, positions[i], positions[i+1])
    svg_parts.append(SVG_FOOTER)
    svg = "\n".join(svg_parts)
    with open(outfile, "w") as f:
        f.write(svg)
