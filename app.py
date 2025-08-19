import os
import streamlit as st

# -------------------------
# Utility: Load SVG file from symbols folder
# -------------------------
def load_svg(name):
    """Load an SVG file from the symbols folder."""
    base_path = os.path.dirname(__file__)  # current script path
    symbols_dir = os.path.join(base_path, "symbols")  # symbols folder
    path = os.path.join(symbols_dir, f"{name.lower().replace(' ', '_')}.svg")
    
    if not os.path.exists(path):
        return f"<rect width='80' height='40' fill='lightgray' stroke='black'/>" \
               f"<text x='5' y='25' font-size='12'>{name}</text>"
    
    with open(path, "r") as f:
        return f.read()

# -------------------------
# Main function to build SVG PFD
# -------------------------
def text_to_svg(process_text):
    steps = [s.strip() for s in process_text.split("->")]
    
    if not steps:
        return None

    svg_elements = []
    x, y = 50, 100
