import re
import os

# ✅ Component keywords mapping
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

# ✅ Draw order
ORDER_PREFERENCE = ['Tank', 'Pump', 'Column', 'Reactor', 'Reboiler', 'Condenser', 'Separator']

# ✅ SVG header/footer
SVG_HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
.text {{ font-family: Arial, sans-serif; font-size: 12px; }}
.conn {{ stroke: #222; stroke-width: 2; fill: none; marker-end: url(#arrow) }}
</style>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L10,5 L0,10 z" />
</marker>
</defs>
'''

SVG_FOOTER = '</svg>\n'

# 📂 SVG symbols folder
SYMBOLS_DIR = "symbols"

# 🔍 Step 1: Extract components
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

# 📐 Step 2: Layout components horizontally
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

# 🖼️ Step 3: Load symbol SVG from file
def load_symbol(symbol_name):
    filename = os.path.join(SYMBOLS_DIR, f"{symbol_name.lower()}.svg")
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        svg_data = f.read()
    inner = re.sub(r'<\?xml.*?\?>', '', svg_data, flags=re.DOTALL)
    inner = re.sub(r'<svg[^>]*>', '', inner, count=1, flags=re.DOTALL)
    inner = re.sub(r'</svg>', '', inner, count=1)
    return inner

# 🧱 Step 4: Draw components
def draw_component(svg_parts, comp):
    x = comp['x']; y = comp['y']; t = comp['type']
    symbol_svg = load_symbol(t)
    if symbol_svg:
        svg_parts.append(f'<g transform="translate({x-40},{y-40}) scale(0.6)">')
        svg_parts.append(symbol_svg)
        svg_parts.append('</g>')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + 60}" text-anchor="middle">{t}</text>')
    else:
        w = 120; h = 70; rx = 8
        left = x - w/2; top = y - h/2
        svg_parts.append(f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="{rx}" fill="#fff" stroke="#222" stroke-width="2"/>')
        svg_parts.append(f'<text class="text" x="{x}" y="{y + h/2 + 8}" text-anchor="middle">{t}</text>')

# 🔗 Step 5: Connect components with lines
def connect(svg_parts, compA, compB):
    x1,y1 = compA['x'], compA['y']
    x2,y2 = compB['x'], compB['y']
    path = f"M{x1},{y1} L{(x1+x2)/2},{y1} L{(x1+x2)/2},{y2} L{x2},{y2}"
    svg_parts.append(f'<path class="conn" d="{path}" />')

# 🎯 Step 6: Main function
def text_to_svg(description, outfile=None):
    comps = extract_components(description)
    if not comps:
        return None
    positions = layout_components(comps)
    width = 1000; height = 500
    svg_parts = [SVG_HEADER.format(w=width, h=height)]
    for p in positions:
        draw_component(svg_parts, p)
    for i in range(len(positions)-1):
        connect(svg_parts, positions[i], positions[i+1])
    svg_parts.append(SVG_FOOTER)
    svg = "\n".join(svg_parts)

    # optional: save file
    if outfile:
        with open(outfile, "w") as f:
            f.write(svg)

    return svg
