import streamlit as st
from text2pfd import text_to_svg
# Mapping keywords in text to symbol file names
SYMBOL_MAP = {
    "pump": "pump.svg",
    "column": "column.svg",
    "distillation": "column.svg",
    "condenser": "condenser.svg",
    "cooler": "cooler.svg",
    "reboiler": "reboiler.svg",
    "reactor": "reactor.svg",
    "tank": "tank.svg" if os.path.exists("symbols/tank.svg") else "column.svg"
}

def text_to_svg(description, outfile="pfd.svg", symbols_dir="symbols"):
    """
    Convert a process description string into a simple left-to-right PFD
    using predefined SVG symbols.
    """

    # Split description by arrows or "→"
    steps = [s.strip().lower() for s in description.replace("→", "->").split("->")]

    # Create a new SVG canvas
    dwg = svgwrite.Drawing(outfile, profile='tiny', size=("1200px", "400px"))

    x, y = 50, 150  # starting position
    step_width = 200  # space between symbols

    for i, step in enumerate(steps):
        symbol_file = None
        for keyword, filename in SYMBOL_MAP.items():
            if keyword in step:
                symbol_file = os.path.join(symbols_dir, filename)
                break

        if symbol_file and os.path.exists(symbol_file):
            # Embed symbol into main SVG
            dwg.add(dwg.image(symbol_file, insert=(x, y), size=("100px", "100px")))
            # Add label below
            dwg.add(dwg.text(step.title(), insert=(x+20, y+120), font_size="12px"))
        else:
            # If no symbol, just draw a box with text
            dwg.add(dwg.rect(insert=(x, y), size=("100px", "100px"),
                             stroke="black", fill="none"))
            dwg.add(dwg.text(step.title(), insert=(x+10, y+55), font_size="12px"))

        # Add arrow to next step
        if i < len(steps) - 1:
            dwg.add(dwg.line(start=(x+100, y+50), end=(x+step_width, y+50),
                             stroke="black", stroke_width=2,
                             marker_end=dwg.marker(refX=2, refY=2,
                             size=(4,4), orient="auto")))

        x += step_width

    # Save diagram
    dwg.save()
    print(f"✅ PFD saved as {outfile}")
