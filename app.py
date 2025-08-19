import streamlit as st
import os

# Load SVG symbols from your /symbols folder
SYMBOLS_DIR = "symbols"
SVG_MAP = {
    "pump": "pump.svg",
    "column": "column.svg",
    "condenser": "cooler.svg",   # using cooler.svg as condenser
    "valve": "valve.svg",
    "heat exchanger": "heat_exchanger.svg",
    "reactor": "reactor.svg",
}

def load_svg(symbol_name):
    """Load an SVG file as string"""
    path = os.path.join(SYMBOLS_DIR, SVG_MAP[symbol_name])
    with open(path, "r") as f:
        return f.read()

def text_to_svg(process_text):
    """Convert text process description into SVG diagram"""
    steps = [s.strip().lower() for s in process_text.split("→")]
    
    # SVG canvas
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400">',
        '<defs>',
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto" markerUnits="strokeWidth">',
        '<path d="M0,0 L0,6 L9,3 z" fill="black"/>',
        '</marker>',
        '</defs>'
    ]
    
    x, y = 50, 150
    step_width = 200
    
    for i, step in enumerate(steps):
        if step in SVG_MAP:
            svg_content = load_svg(step)
            # group with translation
            svg.append(f'<g transform="translate({x}, {y})">{svg_content}</g>')
            # add label
            svg.append(f'<text x="{x+40}" y="{y+120}" font-size="14" text-anchor="middle">{step.title()}</text>')
            
            # draw arrow if not last
            if i < len(steps) - 1:
                svg.append(f'<line x1="{x+100}" y1="{y+60}" x2="{x+step_width}" y2="{y+60}" '
                           f'stroke="black" stroke-width="2" marker-end="url(#arrow)"/>')
            x += step_width
        else:
            svg.append(f'<text x="{x}" y="{y}" fill="red">[Unknown: {step}]</text>')
            x += step_width
    
    svg.append('</svg>')
    return "\n".join(svg)

# ---------------- Streamlit UI ----------------
st.title("Text → PFD Generator")

process_text = st.text_area("Enter process description:", "Pump → Column → Condenser")

if st.button("Generate PFD"):
    svg_code = text_to_svg(process_text)
    st.markdown(svg_code, unsafe_allow_html=True)  # <-- actually render inline SVG
    st.success("✅ PFD generated successfully!")
