import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Project Prakriti - Full Stack AI Analysis",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS
st.markdown('''
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .expert-message {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    .analysis-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
''', unsafe_allow_html=True)

def image_to_base64(image):
    \"\"\"Convert PIL Image to base64\"\"\"
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def call_backend_api(api_key, image_data, region):
    \"\"\"Call Flask backend for analysis\"\"\"
    try:
        # For local development
        backend_url = "http://localhost:5000/analyze"
        
        payload = {
            "api_key": api_key,
            "image_data": image_data,
            "region": region
        }
        
        response = requests.post(backend_url, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        return {"success": False, "error": f"Backend connection failed: {str(e)}"}

def main():
    st.markdown('<h1 class="main-header">🌿 Project Prakriti - Full Stack AI Analysis</h1>', unsafe_allow_html=True)
    
    # API Configuration
    st.sidebar.header("🔐 Gemini API Configuration")
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
    
    st.sidebar.info("""
    **Get Free API Key:**
    1. Visit: https://ai.google.dev/
    2. Create account & get API key
    3. Your key stays in your browser
    """)
    
    if not api_key:
        st.info("👆 Please enter your Gemini API key in the sidebar to start analysis")
        return
    
    # Main interface
    st.header("📸 STEP 1: Upload Plant Image")
    uploaded_file = st.file_uploader(
        "Select a clear plant image for analysis",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a single clear image of the plant"
    )
    
    st.header("🌍 STEP 2: Select Analysis Region")
    region = st.selectbox(
        "Choose Indian State for Regional Analysis",
        ["Maharashtra", "Karnataka", "Madhya Pradesh", "Jharkhand", 
         "Uttarakhand", "Rajasthan", "Kerala"]
    )
    
    # Show image preview
    if uploaded_file:
        st.subheader("📷 Image Preview")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Plant Image", use_column_width=True)
    
    # Analysis button
    if st.button("🚀 Start Full AI Analysis", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("❌ Please upload a plant image")
        elif not api_key:
            st.error("❌ Please enter your Gemini API key")
        else:
            with st.spinner('🔬 Running full AI analysis with Gemini... This may take 30-60 seconds.'):
                try:
                    # Convert image to base64
                    image_data = image_to_base64(image)
                    
                    # Call backend API
                    result = call_backend_api(api_key, image_data, region)
                    
                    if result['success']:
                        st.success("✅ Full AI Analysis Complete!")
                        st.balloons()
                        
                        # Display Species Analysis
                        st.subheader("🌿 Species Identification")
                        with st.expander("View Detailed Species Analysis", expanded=True):
                            st.write(result['species_analysis'])
                        
                        # Expert Analyses
                        st.subheader("💬 AI Expert Analysis")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("### 🌤️ Climate Expert")
                            st.markdown(f'<div class="expert-message">{result["climate_analysis"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("### 🌿 Biodiversity Expert") 
                            st.markdown(f'<div class="expert-message">{result["biodiversity_analysis"]}</div>', unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown("### 🔨 Restoration Expert")
                            st.markdown(f'<div class="expert-message">{result["restoration_analysis"]}</div>', unsafe_allow_html=True)
                        
                        # Regional Data
                        st.subheader("🌡️ Regional Analysis")
                        region_data = result['region_data']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Climate Type", region_data.get('climate', 'Unknown'))
                            st.metric("Temperature Range", region_data.get('temperature', 'Unknown'))
                            st.metric("Rainfall", region_data.get('rainfall', 'Unknown'))
                        
                        with col2:
                            st.metric("Soil Types", ", ".join(region_data.get('soil_types', [])))
                            st.metric("Soil pH", region_data.get('soil_ph', 'Unknown'))
                            st.metric("Biodiversity", region_data.get('biodiversity', 'Unknown'))
                        
                        # Raw JSON for debugging
                        with st.expander("📊 View Raw API Response"):
                            st.json(result)
                            
                    else:
                        st.error(f"❌ Analysis failed: {result['error']}")
                        st.info("Please check your API key and try again with a clear plant image.")
                        
                except Exception as e:
                    st.error(f"❌ Analysis error: {str(e)}")
                    st.info("""
                    **Troubleshooting tips:**
                    - Make sure your Flask backend is running
                    - Check your API key is valid
                    - Try with a different plant image
                    - Ensure you have stable internet connection
                    """)

if __name__ == "__main__":
    main()
