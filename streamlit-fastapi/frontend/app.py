import streamlit as st
import requests

# Page configuration - sets the browser tab title and layout
st.set_page_config(
    page_title="Name Analysis Tool",
    layout="wide"
)

# Header - styled with custom CSS
st.markdown("""
<div class="main-header">
    <h1>🔍 Name Analysis Tool</h1>
    <p>Discover insights about any name using AI predictions</p>
</div>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000"  # Base URL for the FastAPI backend

def analyze_name(name):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze-name",
            json={"name": name},
            timeout=10
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        return None

# Main form section
with st.form("name_form"):
    st.subheader("Enter a Name to Analyze")
    # Text input for the user to enter a name
    name = st.text_input("Name:", placeholder="Type a name here...")
    # Submit button that triggers the form
    submitted = st.form_submit_button("Analyze Name", use_container_width=True)

# Process the form when submitted
if submitted and name.strip():  # Only proceed if form submitted AND name isn't empty
    # Show spinner while processing
    with st.spinner("Analyzing name..."):
        result = analyze_name(name.strip())
    
    # If we got results back from the API
    if result:
        st.success(f"Analysis complete for: **{result['name']}**")
        
        # Create three columns for displaying results side by side
        col1, col2, col3 = st.columns(3)
        
        # Age prediction column
        with col1:
            st.markdown("""
            <div class="result-card">
                <h3>🎂 Predicted Age</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if result['age']:
                st.metric("Age", f"{result['age']} years old")
            else:
                st.info("No age prediction available")
        
        # Gender prediction column
        with col2:
            st.markdown("""
            <div class="result-card">
                <h3>👤 Predicted Gender</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if result['gender']:
                gender_display = result['gender'].capitalize()  # Capitalize first letter
                # Show confidence percentage if available
                confidence = f"{result['probability'] * 100:.1f}%" if result['probability'] else "N/A"
                st.metric("Gender", gender_display, f"Confidence: {confidence}")
            else:
                st.info("No gender prediction available")

                # Nationality prediction column
        with col3:
            st.markdown("""
            <div class="result-card">
                <h3>🌍 Likely Nationality</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if result['countries']:
                # Show the top country prediction
                top_country = result['countries'][0]
                country_code = top_country['country_id']
                probability = top_country['probability'] * 100
                st.metric("Country", country_code, f"{probability:.1f}% confidence")
            else:
                st.info("No nationality prediction available")