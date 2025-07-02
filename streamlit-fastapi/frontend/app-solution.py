import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Random Dog Generator",
    page_icon="🐕",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
}
.dog-container {
    text-align: center;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Random Dog Generator</h1>
    <p>Get adorable random dog images from our FastAPI backend!</p>
</div>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state for dog image
if 'dog_image_url' not in st.session_state:
    st.session_state.dog_image_url = None
if 'loading' not in st.session_state:
    st.session_state.loading = False

def fetch_random_dog():
    """Fetch a random dog image from the FastAPI backend"""
    try:
        with st.spinner('Fetching a cute dog for you...'):
            response = requests.get(f"{API_BASE_URL}/api/random-dog", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data['imageUrl'], None
            else:
                return None, f"Error: {response.status_code} - {response.text}"
                
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the FastAPI server. Make sure it's running on http://localhost:8000"
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Generate Random Dog Images")
    
    # Button to fetch new dog
    if st.button("Get New Random Dog!", type="primary", use_container_width=True):
        st.session_state.loading = True
        image_url, error = fetch_random_dog()
        
        if error:
            st.error(error)
        else:
            st.session_state.dog_image_url = image_url
        
        st.session_state.loading = False
    
    # Auto-fetch on first load
    if st.session_state.dog_image_url is None and not st.session_state.loading:
        with st.spinner('Loading your first dog...'):
            image_url, error = fetch_random_dog()
            if not error:
                st.session_state.dog_image_url = image_url
            else:
                st.error(error)

# Display the dog image
if st.session_state.dog_image_url:
    st.markdown("---")
    st.markdown("### Your Random Dog:")
    
    # Center the image
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        try:
            st.image(
                st.session_state.dog_image_url, 
                caption="Adorable random dog! 🐕",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Could not load image: {str(e)}")