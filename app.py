import streamlit as st
from text2pfd import text_to_svg

st.set_page_config(page_title="Text to PFD Generator", layout="wide")

st.title("🛠 Text → Process Flow Diagram Generator")

st.markdown("""
Enter a simple description of your process (e.g.  
*Feed tank → Pump → Distillation Column → Reboiler & Condenser*).  
The app will generate a basic PFD for you.
""")

description = st.text_area("Process Description:", 
    "Feed from feed tank via pump feeds a distillation column. Reboiler at bottom. Overhead goes to condenser and reflux pump.")

if st.button("Generate PFD"):
    outfile = "pfd.svg"
    text_to_svg(description, outfile=outfile)
    with open(outfile, "r") as f:
        svg_data = f.read()

    st.success("✅ Diagram generated below:")
    st.image(outfile)   # preview PNG rendering
    st.download_button("📥 Download SVG", data=svg_data, file_name="pfd.svg", mime="image/svg+xml")
