import os

# Define known symbols mapping to your SVG files in /symbols folder
SYMBOLS = {
    "pump": "symbols/pump.svg",
    "column": "symbols/column.svg",
    "condenser": "symbols/condenser.svg",
    "cooler": "symbols/cooler.svg",
    "reactor": "symbols/reactor.svg",
    "reboiler": "symbols/reboiler.svg"
}

def load_svg(path, x, y):
    """Load an SVG file and wrap it with translation."""
    if not os.path.exists(path):
        return f'<rect x="{x}" y="{y}" width="80" height="50" fill="lightgray" stroke="black"/>'
    with open(path, "r") as f:
        svg_content = f.read()
    # remove existing outer <svg> tags
    svg_content = svg_content.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    svg_content = svg_content.replace("<svg", "<g")
    svg_content = svg_content.replace("</svg>", "</g>")
    return f'<g transform="translate({x},{y}) scale(0.5)">{svg_content}</g>'

def text_to_svg(description, outfile=None):
    """Convert a text process description into an SVG diagram with arr
