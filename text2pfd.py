import os

SYMBOLS_DIR = "symbols"   # folder where your SVG symbol files are stored

def text_to_svg(description, outfile="pfd.svg"):
    """
    Convert a process description (like 'Pump → Column → Condenser')
    into an SVG diagram using symbols stored in SYMBOLS_DIR.
    """

    components = [c.strip() for c in description.split("→")]
    if not components or components == [""]:
        return None

    svg_elements = []
    x, y = 50, 50
    spacing = 200

    for i, comp in enumerate(components):
        # normalize to lowercase for matching
        key = comp.lower()
        svg_file = os.path.join(SYMBOLS_DIR, f"{key}.svg")

        if os.path.exists(svg_file):
            # ✅ load symbol SVG file
            with open(svg_file, "r") as f:
                symbol_svg = f.read()
            # shift symbol position
            symbol_svg = symbol_svg.replace("<svg", f"<svg x='{x}' y='{y}'")
            svg_elements.append(symbol_svg)
        else:
            # ⚠️ fallback to rectangle + label
            rect = f"<rect x='{x}' y='{y}' width='100' height='60' fill='white' stroke='black'/>"
            label = f"<text x='{x+50}' y='{y+80}' text-anchor='middle' font-size='14'>{comp}</text>"
            svg_elements.append(rect + label)

        # ➡️ draw arrow to next component
        if i < len(components) - 1:
            arrow = f"<line x1='{x+100}' y1='{y+30}' x2='{x+spacing-20}' y2='{y+30}' stroke='black' marker-end='url(#arrow)'/>"
            svg_elements.append(arrow)

        x += spacing

    # wrap everything in an SVG container
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width='{x+100}' height='200'>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto">
            <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
    </defs>
    {''.join(svg_elements)}
    </svg>"""

    with open(outfile, "w") as f:
        f.write(svg_content)

    return svg_content
