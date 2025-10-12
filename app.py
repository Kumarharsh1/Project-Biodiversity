import streamlit as st
import sys
import os
from PIL import Image
import requests
import json

# Add the api directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

st.set_page_config(
    page_title="Project Prakriti - Biodiversity Analysis",
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
    .upload-area {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .result-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #2e7d32;
    }
</style>
''', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌿 Project Prakriti - Biodiversity Analysis</h1>', unsafe_allow_html=True)
    
    st.write("Upload plant images and select a region for advanced ecological analysis powered by AI.")
    
    # File upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 STEP 1: Upload Plant Images")
        uploaded_files = st.file_uploader(
            "Select 1-4 plant images",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            key="file_uploader"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} image(s) selected")
            
            # Show image previews
            cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Image {i+1}", width=150)
    
    with col2:
        st.subheader("🌍 STEP 2: Select Region")
        region = st.selectbox(
            "Choose Indian State",
            ["", "Madhya Pradesh", "Maharashtra", "Karnataka", "Jharkhand", 
             "Uttarakhand", "Rajasthan", "Kerala"],
            key="region_select"
        )
    
    # Analysis button
    analyze_btn = st.button(
        "🚀 Start Enhanced Analysis",
        type="primary",
        disabled=not (uploaded_files and region),
        use_container_width=True
    )
    
    if analyze_btn:
        with st.spinner('🔬 Running advanced analysis with AI... This may take a few moments.'):
            # Simulate analysis (replace with actual API call)
            import time
            time.sleep(3)
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Species Identification
            with st.expander("🌿 Species Identification Results", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Common Name", "Neem Tree")
                    st.metric("Scientific Name", "Azadirachta indica")
                    st.metric("Family", "Meliaceae")
                with col2:
                    st.metric("Confidence", "92%")
                    st.metric("Method", "AI-Powered Analysis")
            
            # Expert Analysis
            with st.expander("💬 Expert Agent Conversation", expanded=True):
                tab1, tab2, tab3 = st.tabs(["🌤️ Climate Expert", "🌿 Biodiversity Expert", "🔨 Restoration Expert"])
                
                with tab1:
                    st.info("Based on climate analysis, the conditions in " + region + " are optimal for this species. Temperature range and rainfall patterns align perfectly with natural habitat requirements.")
                
                with tab2:
                    st.info("This species has high ecological value and will significantly enhance local biodiversity. Recommend companion planting with native species for maximum ecosystem benefits.")
                
                with tab3:
                    st.info("Excellent insights from both experts. Recommend phased restoration approach beginning next growing season. Expected timeline shows significant ecological benefits within 2-3 years.")
            
            # Climate & Soil Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container():
                    st.subheader("🌡️ Climate Analysis")
                    st.metric("Climate Type", "Subtropical")
                    st.metric("Temperature", "20-38°C")
                    st.metric("Rainfall", "1000-1600mm")
                    st.metric("Growing Season", "Kharif (June-Oct)")
            
            with col2:
                with st.container():
                    st.subheader("🏔️ Soil Compatibility")
                    st.metric("Soil Types", "Black, Alluvial")
                    st.metric("Soil pH", "6.0-8.0")
                    st.metric("Compatibility", "Excellent")
                    st.metric("Restoration Potential", "High")

if __name__ == "__main__":
    main()
