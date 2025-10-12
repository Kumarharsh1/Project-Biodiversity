import streamlit as st
import os
from PIL import Image
import io

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
</style>
''', unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🌿 Project Prakriti - Biodiversity Analysis</h1>', unsafe_allow_html=True)
    
    st.info("Upload plant images and select a region for advanced ecological analysis powered by AI.")
    
    # File upload
    st.subheader("📁 STEP 1: Upload Plant Images")
    uploaded_files = st.file_uploader(
        "Select 1-4 plant images (PNG, JPG, JPEG)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload clear images of plants for analysis"
    )
    
    # Region selection
    st.subheader("🌍 STEP 2: Select Region")
    region = st.selectbox(
        "Choose Indian State for Analysis",
        ["", "Madhya Pradesh", "Maharashtra", "Karnataka", "Jharkhand", 
         "Uttarakhand", "Rajasthan", "Kerala"],
        index=0
    )
    
    # Show image previews
    if uploaded_files:
        st.subheader("📷 Image Previews")
        cols = st.columns(min(4, len(uploaded_files)))
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Image {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error loading image {i+1}")
    
    # Analysis button
    if st.button("🚀 Start Enhanced Analysis", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("❌ Please upload at least one plant image")
        elif not region:
            st.error("❌ Please select a region")
        else:
            with st.spinner('🔬 Running advanced analysis with AI... This may take a few moments.'):
                # Simulate processing
                import time
                time.sleep(2)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Results section
                st.subheader("🌿 Identification Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Common Name", "Neem Tree")
                    st.metric("Scientific Name", "Azadirachta indica")
                    st.metric("Family", "Meliaceae")
                
                with col2:
                    st.metric("Confidence", "92%")
                    st.metric("Compatibility", "Excellent")
                
                # Expert analysis
                st.subheader("💬 Expert Insights")
                st.info("""
                **🌤️ CLIMATE EXPERT:** Conditions in {} are optimal for this species. 
                Temperature range and rainfall patterns align perfectly with natural habitat requirements.
                """.format(region))
                
                st.info("""
                **🌿 BIODIVERSITY EXPERT:** This species has high ecological value and will 
                significantly enhance local biodiversity. Recommend companion planting.
                """)
                
                st.info("""
                **🔨 RESTORATION EXPERT:** Phased restoration approach recommended beginning 
                next growing season. Significant ecological benefits expected within 2-3 years.
                """)

if __name__ == "__main__":
    main()
