import os

SYMBOLS_DIR = "symbols"

# Map keywords to symbol filenames
COMPONENT_MAP = {
    "pump": "pump.svg",
    "column": "column.svg",
    "condenser": "cooler.svg",
    "valve": "valve.svg",
    "heat exchanger": "heat_exchanger.svg",
    "reactor": "reactor.svg",
}

def load_svg_symbol(name):
    """Load SVG file content from symbols/ folder"""
    filepath = os.path.join(SYMBOLS_DIR, name)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    return None

def text_to_svg(description):
    components = [c.strip().lower() for c in description.split("→")]

    if not components:
        return None

    svg_elements = []
    x, y = 50, 100
    spacing = 200

    # Add arrow marker definition
    arrow_def = """
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3"
              orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="black"/>
      </marker>
    </defs>
    """

    for i, comp in enumerate(components):
        symbol_file = None
        for key, filename in COMPONENT_MAP.items():
            if key in comp:
                symbol_file = filename
                break

        if symbol_file:
            svg_symbol = load_svg_symbol(symbol_file)
            if svg_symbol:
                # Place symbol inside <g> with transform
                svg_elements.append(f'<g transform="translate({x},{y})">{svg_symbol}</g>')
                # Add label text
                svg_elements.append(f'<text x="{x+40}" y="{y+120}" text-anchor="middle" font-size="14">{comp.title()}</text>')
        else:
            # Fallback rectangle
            svg_elements.append(f'<rect x="{x}" y="{y}" width="80" height="60" fill="lightgray" stroke="black"/>')
            svg_elements.append(f'<text x="{x+40}" y="{y+35}" text-anchor="middle" font-size="14">{comp.title()}</text>')

        # Add arrow to next component
        if i < len(components) - 1:
            svg_elements.append(f'<line x1="{x+80}" y1="{y+30}" x2="{x+spacing}" y2="{y+30}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>')

        x += spacing

    svg_code = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{x+100}" height="300">
      {arrow_def}
      {''.join(svg_elements)}
    </svg>
    """

    return svg_code
