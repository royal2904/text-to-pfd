import streamlit as st
from text2pfd import text_to_svg

st.title("Process Flow Diagram Generator")

description = st.text_area("Enter process description:")

if st.button("Generate PFD"):
    svg_code = text_to_svg(description)
    if svg_code:
        st.markdown(svg_code, unsafe_allow_html=True)  # show diagram
        st.success("✅ PFD generated successfully!")
    else:
        st.warning("⚠️ No valid components detected.")
