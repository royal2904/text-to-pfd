import streamlit as st
from text2pfd import text_to_svg

# 🎨 Page Config
st.set_page_config(
    page_title="Process Flow Diagram Generator",
    page_icon="⚙️",
    layout="centered"
)

# 🎨 Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f9fafb;
        padding: 20px;
        border-radius: 12px;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .pfd-box {
        background: white;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏷️ Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>⚙️ Process Flow Diagram Generator</h1>", unsafe_allow_html=True)

# 📌 Sidebar
with st.sidebar:
    st.header("📘 How to use")
    st.write("1. Enter a process description (e.g., *Feed tank → Pump → Column → Condenser*).")
    st.write("2. Click **Generate PFD**.")
    st.write("3. View your generated process flow diagram below.")
    st.info("💡 Make sure SVG symbol files exist in the **symbols/** folder!")

# 📝 Input
description = st.text_area("✍️ Enter process description:")

# 🔘 Button
if st.button("🚀 Generate PFD"):
    svg_code = text_to_svg(description)
    if svg_code:
        st.markdown('<div class="pfd-box">', unsafe_allow_html=True)
        st.markdown(svg_code, unsafe_allow_html=True)  # show diagram
        st.markdown('</div>', unsafe_allow_html=True)
        st.success("✅ PFD generated successfully!")
    else:
        st.warning("⚠️ No valid components detected.")
