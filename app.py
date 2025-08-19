import streamlit as st
from text2pfd import text_to_svg

st.set_page_config(page_title="Process Flow Diagram Generator", layout="wide")

st.title("🛠 Text → Process Flow Diagram Generator")

st.markdown("""
Enter a simple description of your process (example):  
**Feed Tank → Pump → Column → Reboiler & Condenser**
""")

description = st.text_area("Process Description:", "Pump → Column → Condenser")

if st.button("Generate PFD"):
    svg_code = text_to_svg(description)
    if svg_code:
        st.markdown(svg_code, unsafe_allow_html=True)
        st.success("✅ PFD generated successfully!")
    else:
        st.warning("⚠️ No valid components detected.")
