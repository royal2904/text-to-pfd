import os

# Path to your symbols folder
SYMBOLS_DIR = os.path.join(os.path.dirname(__file__), "symbols")

# Mapping of text keywords → SVG filenames
COMPONENT_MAP = {
    "pump": "pump.svg",
    "column": "column.svg",
    "distillation column": "column.svg",
    "condenser": "heat_exchanger.svg",
    "cooler": "cooler.svg",
    "reactor": "reactor.svg",
    "heat exchanger": "heat_exchanger.svg",
    "valve": "valve.svg",
}

def load_symbol(name):
    """
    Load SVG content for a given component name.
    """
    filename = COMPONENT_MAP.get(name.lower())
    if not filename:
        return None

    filepath = os.path.join(SYMBOLS_DIR, filename)
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    

def text_to_svg(description, outfile="pfd.svg"):
    """
    Convert a text description (→ separated) into a PFD SVG string.
    """
    steps = [s.strip().lower() for s in description.split("→")]
    if not
