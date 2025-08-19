import os

SYMBOLS_DIR = "symbols"  # folder where all SVG symbol files are stored

def load_symbol(symbol_name):
    """Load an SVG file from symbols folder, fallback to rectangle if missing."""
    file_path = os.path.join(SYMBOLS_DIR, f"{symbol_name.lower()}.svg")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    else:
        # fallback rectangle with text
        return f'''
        <rect width="100" height="50" style="fill:none;stroke:black;stroke-width:2"/>
        <text x="10" y="30" font-size="14">{symbol_name}</text>
        '''

def text_to_svg(description):
    """Convert text description into SVG diagram using custom symbols and arrows."""
    components = [c.strip() for c in description.split("→") if c.strip()]
    
    svg_elements = []
    x_offset = 20
    y_offset = 80
    symbol_width = 120   # space reserved per symbol
    arrow_gap = 40       # gap between symbol edge and arrow
    
    for i, comp in enumerate(components):
        # Load SVG for symbol
        symbol_svg = load_symbol(comp)
        
        # Place the symbol in position
        svg_elements.append(f'<g transform="translate({x_offset},{y_offset})">{symbol_svg}</g>')
