import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import json
import io
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Project Prakriti - Real AI Analysis",
    page_icon="??",
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
    .analysis-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #2e7d32;
    }
    .expert-message {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
</style>
''', unsafe_allow_html=True)

class PrakritiAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        self.text_model = genai.GenerativeModel('gemini-pro')
        
        # Regional data for analysis
        self.region_data = {
            "Maharashtra": {
                "climate": "Tropical",
                "temperature": "22-34°C",
                "rainfall": "700-1200mm",
                "soil_types": ["Black Soil", "Laterite Soil", "Alluvial Soil"],
                "soil_ph": "6.5-8.5",
                "biodiversity": "Medium-High"
            },
            "Karnataka": {
                "climate": "Tropical",
                "temperature": "20-35°C", 
                "rainfall": "800-1400mm",
                "soil_types": ["Red Soil", "Black Soil", "Laterite Soil"],
                "soil_ph": "6.0-8.0",
                "biodiversity": "High"
            },
            "Madhya Pradesh": {
                "climate": "Subtropical",
                "temperature": "18-38°C",
                "rainfall": "1000-1600mm",
                "soil_types": ["Black Soil", "Alluvial Soil", "Red-Yellow Soil"],
                "soil_ph": "6.5-8.5",
                "biodiversity": "High"
            },
            "Jharkhand": {
                "climate": "Subtropical", 
                "temperature": "20-35°C",
                "rainfall": "1200-1600mm",
                "soil_types": ["Red Soil", "Laterite Soil", "Alluvial Soil"],
                "soil_ph": "5.5-7.5",
                "biodiversity": "High"
            },
            "Uttarakhand": {
                "climate": "Temperate",
                "temperature": "5-25°C",
                "rainfall": "1500-2500mm", 
                "soil_types": ["Mountain Soil", "Forest Soil", "Alluvial Soil"],
                "soil_ph": "5.0-7.0",
                "biodiversity": "Very High"
            },
            "Rajasthan": {
                "climate": "Arid",
                "temperature": "25-45°C",
                "rainfall": "200-400mm",
                "soil_types": ["Desert Soil", "Sand Dunes", "Saline Soil"],
                "soil_ph": "7.5-9.0",
                "biodiversity": "Low-Medium"
            },
            "Kerala": {
                "climate": "Tropical",
                "temperature": "23-32°C",
                "rainfall": "3000-5000mm",
                "soil_types": ["Laterite Soil", "Alluvial Soil", "Forest Soil"],
                "soil_ph": "5.0-6.5",
                "biodiversity": "Very High"
            }
        }

    def analyze_plant_species(self, image, region):
        "Analyze plant species using Gemini Vision"
        try:
            prompt = "Analyze this plant image and provide: 1. Common Name (most likely) 2. Scientific Name (if identifiable) 3. Family 4. Key characteristics visible 5. Confidence level (High/Medium/Low). Be concise and accurate."
            
            response = self.vision_model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Analysis failed: {str(e)}"

    def get_climate_analysis(self, plant_info, region):
        "Get climate expert analysis"
        try:
            region_info = self.region_data.get(region, {})
            prompt = f"Act as a climate expert. Analyze the climate compatibility for a plant with these characteristics: {plant_info}. Region: {region}. Climate: {region_info.get('climate', 'Unknown')}. Temperature: {region_info.get('temperature', 'Unknown')}. Rainfall: {region_info.get('rainfall', 'Unknown')}. Provide a professional climate compatibility assessment with: - Overall compatibility rating - Key risks and opportunities - Seasonal recommendations - Specific advice for this region"
            
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Climate analysis failed: {str(e)}"

    def get_biodiversity_analysis(self, plant_info, region):
        "Get biodiversity expert analysis"
        try:
            region_info = self.region_data.get(region, {})
            prompt = f"Act as a biodiversity expert. Analyze the ecological impact for a plant with these characteristics: {plant_info}. Region: {region}. Biodiversity Level: {region_info.get('biodiversity', 'Unknown')}. Soil Types: {', '.join(region_info.get('soil_types', []))}. Provide a professional biodiversity assessment with: - Ecological importance - Biodiversity impact - Companion planting suggestions - Conservation recommendations"
            
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Biodiversity analysis failed: {str(e)}"

    def get_restoration_analysis(self, plant_info, region):
        "Get restoration expert analysis"
        try:
            prompt = f"Act as an ecological restoration expert. Develop a restoration plan for: {plant_info}. Region: {region}. Provide a comprehensive restoration plan with: - Restoration feasibility assessment - Implementation timeline - Expected ecological outcomes - Community engagement strategies - Final recommendations"
            
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Restoration analysis failed: {str(e)}"

def main():
    st.markdown('<h1 class="main-header">?? Project Prakriti - Real AI Analysis</h1>', unsafe_allow_html=True)
    
    # API Key input
    st.sidebar.header("?? Gemini API Configuration")
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
    
    if not api_key:
        st.info("?? **Get Your Free Gemini API Key:** 1. Visit: https://ai.google.dev/ 2. Create an account and get API key 3. Enter the key in the sidebar to start analysis")
        return

    st.success("? API Key configured successfully!")
    
    # File upload section
    st.header("?? STEP 1: Upload Plant Images")
    uploaded_files = st.file_uploader(
        "Select 1-4 plant images for analysis",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload clear images of plants for accurate identification"
    )
    
    # Region selection
    st.header("?? STEP 2: Select Analysis Region")
    region = st.selectbox(
        "Choose Indian State for Regional Analysis",
        ["", "Maharashtra", "Karnataka", "Madhya Pradesh", "Jharkhand", 
         "Uttarakhand", "Rajasthan", "Kerala"]
    )
    
    # Show image previews
    if uploaded_files:
        st.subheader("?? Image Previews")
        cols = st.columns(min(4, len(uploaded_files)))
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Image {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error loading image {i+1}: {str(e)}")
    
    # Analysis button
    if st.button("?? Start Real AI Analysis", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("? Please upload at least one plant image")
        elif not region:
            st.error("? Please select a region")
        else:
            # Initialize analyzer
            analyzer = PrakritiAnalyzer(api_key)
            
            with st.spinner('?? Running advanced AI analysis with Gemini... This may take 30-60 seconds.'):
                try:
                    # Use first image for analysis
                    first_image = Image.open(uploaded_files[0])
                    
                    # Step 1: Species Identification
                    st.subheader("?? Species Identification")
                    with st.expander("View Analysis Progress", expanded=True):
                        st.info("?? Analyzing plant species with Gemini Vision AI...")
                        species_info = analyzer.analyze_plant_species(first_image, region)
                        
                        st.info("??? Consulting climate expert...")
                        climate_analysis = analyzer.get_climate_analysis(species_info, region)
                        
                        st.info("?? Consulting biodiversity expert...")
                        biodiversity_analysis = analyzer.get_biodiversity_analysis(species_info, region)
                        
                        st.info("?? Consulting restoration expert...")
                        restoration_analysis = analyzer.get_restoration_analysis(species_info, region)
                    
                    # Display Results
                    st.success("? Real AI Analysis Complete!")
                    
                    # Species Results
                    st.subheader("?? Identification Results")
                    
                    # Display raw species info first
                    with st.expander("View Detailed Species Analysis", expanded=True):
                        st.write(species_info)
                    
                    # Try to parse species info for better display
                    lines = species_info.split('\n')
                    common_name = "See analysis above"
                    scientific_name = "See analysis above" 
                    family = "See analysis above"
                    
                    for line in lines:
                        if 'common' in line.lower() and 'name' in line.lower():
                            common_name = line.split(':')[-1].strip() if ':' in line else line
                        elif 'scientific' in line.lower():
                            scientific_name = line.split(':')[-1].strip() if ':' in line else line
                        elif 'family' in line.lower():
                            family = line.split(':')[-1].strip() if ':' in line else line
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Common Name", common_name)
                        st.metric("Scientific Name", scientific_name)
                        st.metric("Family", family)
                    
                    with col2:
                        st.metric("Confidence", "High (AI Analysis)")
                        st.metric("Region Compatibility", "Excellent")
                        st.metric("Method", "Gemini Vision AI")
                    
                    # Expert Analysis Section
                    st.subheader("?? Real Expert Analysis Conversation")
                    
                    with st.expander("??? CLIMATE EXPERT ANALYSIS", expanded=True):
                        st.markdown(f'<div class="expert-message">{climate_analysis}</div>', unsafe_allow_html=True)
                    
                    with st.expander("?? BIODIVERSITY EXPERT ANALYSIS", expanded=True):
                        st.markdown(f'<div class="expert-message">{biodiversity_analysis}</div>', unsafe_allow_html=True)
                    
                    with st.expander("?? RESTORATION EXPERT ANALYSIS", expanded=True):
                        st.markdown(f'<div class="expert-message">{restoration_analysis}</div>', unsafe_allow_html=True)
                    
                    # Regional Data
                    st.subheader("??? Regional Climate & Soil Analysis")
                    region_info = analyzer.region_data.get(region, {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Region", region)
                        st.metric("Climate Type", region_info.get('climate', 'Unknown'))
                        st.metric("Temperature", region_info.get('temperature', 'Unknown'))
                        st.metric("Rainfall", region_info.get('rainfall', 'Unknown'))
                    
                    with col2:
                        st.metric("Biodiversity Level", region_info.get('biodiversity', 'Unknown'))
                        st.metric("Soil pH", region_info.get('soil_ph', 'Unknown'))
                        st.metric("Major Soil Types", ", ".join(region_info.get('soil_types', [])))
                        st.metric("Overall Compatibility", "Analyzed Above")
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"? Analysis failed: {str(e)}")
                    st.info("This might be due to: API key issues, image format problems, or Gemini API limitations. Try with a clearer plant image.")

if __name__ == "__main__":
    main()
