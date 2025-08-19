import os

SYMBOLS_FOLDER = "symbols"

COMPONENT_MAP = {
    "pump": "pump.svg",
    "column": "column.svg",
    "distillation column": "column.svg",
    "condenser": "condenser.svg",
    "cooler": "cooler.svg",
    "reactor": "reactor.svg",
    "reboiler": "reboiler.svg",
    "feed tank": "feed_tank.svg",
}

def load_svg(filename):
    path = os.path.join(SYMBOLS_FOLDER, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return None

def text_to_svg(description, outfile=None):
    if not description:
        return None

    steps = [s.strip().lower() for s in description.replace("→", "->").split("->")]

    x, y = 50, 100
    dx = 250
    svg_elements = []

    svg_header = """
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600">
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3"
                orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
      </defs>
    """
    svg_elements.append(svg_header)

    prev_x, prev_y = None, None

    for step in steps:
        symbol_file = None
        for key, filename in COMPONENT_MAP.items():
            if key in step:
                symbol_file = filename
                break

        if symbol_file:
            svg_code = load_svg(symbol_file)
            if svg_code:
                svg_elements.append(f'<g transform="translate({x},{y}) scale(0.5)">')
                svg_elements.append(svg_code)
                svg_elements.append("</g>")

        if prev_x is not None:
            line = f'<line x1="{prev_x+100}" y1="{prev_y+50}" x2="{x}" y2="{y+50}" ' \
                   f'stroke="black" stroke-width="2" marker-end="url(#arrow)" />'
            svg_elements.append(line)

        prev_x, prev_y = x, y
        x += dx

    svg_elements.append("</svg>")
    final_svg = "\n".join(svg_elements)

    if outfile:
        with open(outfile, "w") as f:
            f.write(final_svg)

    return final_svg
