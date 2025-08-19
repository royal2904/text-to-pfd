import os
import re

# Folder where your SVG symbols are stored
SYMBOLS_DIR = "symbols"

def normalize_name(name: str) -> str:
    """Normalize component names to match SVG filenames."""
    return name.strip().lower().replace(" ", "")

def load_symbol(symbol_name: str) -> str:
    """Load SVG symbol file if available, else return a rectangle fallback."""
    filename = f"{normalize_name(symbol_name)}.svg"
    filepath = os.path.join(SYMBOLS_DIR, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    else:
        # fallback block if svg missing
        return f'<rect width="100" height="50" fill="lightgrey" stroke="black"/>' \
               f'<text x="10" y="25" font-size="12">{symbol_name}</text>'

def text_to_svg(description: str, outfile: str = None) -> str:
    """
    Convert text description to SVG process flow diagram.
    Example input: "Pump → Column → Condenser"
    """

    # Split description into components
    components = re.split(r"→|->|-->|-", description)
    components = [c.strip() for c in components if c.strip()]

    if not components:
        return None

    # SVG canvas size (can be adjusted)
    width = 200 * len(components)
    height = 200

    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']

    x, y = 50, 80
    spacing = 200

    for i, comp in enumerate(components):
        symbol_svg = load_symbol(comp)

        # Wrap each symbol in a group with translation
        svg_parts.append(f'<g transform="translate({x},{y})">{symbol_svg}</g>')

        # Add arrow to next symbol
        if i < len(components) - 1:
            arrow_x1 = x + 100
            arrow_x2 = x + spacing
            arrow_y = y + 25
            svg_parts.append(
                f'<line x1="{arrow_x1}" y1="{arrow_y}" x2="{arrow_x2 - 20}" y2="{arrow_y}" '
                f'stroke="black" marker-end="url(#arrow)"/>'
            )

        x += spacing

    # Define arrow marker
    arrow_marker = """
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3"
              orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="black"/>
      </marker>
    </defs>
    """
    svg_parts.insert(1, arrow_marker)

    svg_parts.append("</svg>")

    svg_code = "\n".join(svg_parts)

    if outfile:
        with open(outfile, "w") as f:
            f.write(svg_code)

    return svg_code
