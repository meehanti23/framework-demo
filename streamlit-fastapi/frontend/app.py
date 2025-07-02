import streamlit as st
import requests

# Page configuration - sets the browser tab title and layout
st.set_page_config(
    page_title="Dog Image Generator",
    layout="wide"
)

# Header - styled with custom CSS
st.markdown("""
<div class="main-header">
    <h1>Dog Image Generator</h1>
    <p>Generate Random Image of a Dog</p>
</div>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000"  # Base URL for the FastAPI backend