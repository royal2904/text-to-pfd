import os
import streamlit as st

# -------------------------
# Paths & Setup
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOLS_DIR = os.path.join(BASE_DIR, "symbols")

# Map process step names to their SVG files
SVG_MAP = {
    "pump": "pump.svg",
    "cooler": "cooler.svg",
    "column": "column.svg",
    "valve": "valve.svg",
    "heat exchanger": "heat_exchanger.svg",
    "reactor": "reactor.svg"
}

# -------------------------
# Functions
# -------------------------
def load_svg(symbol_name):
    """Load an SVG file as string"""
    if symbol_name not in SVG_MAP:
        return f"<text x='0' y='0' fill='red'>Unknown: {symbol_name}</text>"

    file_name = SVG_MAP[symbol_name]
    path = os.path.join(SYMBOLS_DIR, file_name)

    if not os.path.exists(path):
        return f"<text x='0' y='0' fill='red'>Missing: {file_name}</text>"

    with open(path, "r") as f:
        return f.read()


def text_to_svg(process_text):
    """Convert text input into SVG diagram"""
    steps = [s.strip().lower() for s in process_text.split("->")]

    svg_elements = []
    x, y = 50, 100

    for step in steps:
        svg_content = load_svg(step)
        svg_elements.append(f"<g transform='translate({x},{y})'>{svg_content}</g>")

        # Add step name below symbol
        svg_elements.append(
            f"<text x='{x+40}' y='{y+120}' font-size='14' text-anchor='middle' fill='black'>{step.title()}</text>"
        )

        # Draw arrow to next step
        x += 180
        svg_elements.append(
            f"<line x1='{x-100}' y1='{y+30}' x2='{x-20}' y2='{y+30}' "
            f"stroke='black' stroke-width='2' marker-end='url(#arrow)'/>"
        )

    # Combine into final SVG
    svg_code = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{x+100}" height="300">
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3"
                orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
      </defs>
      {''.join(svg_elements)}
    </svg>
    """
    return svg_code


# -------------------------
# Streamlit UI
# -------------------------
st.title("Text to PFD Generator")

process_text = st.text_area("Enter process steps (e.g. Pump -> Heat Exchanger -
