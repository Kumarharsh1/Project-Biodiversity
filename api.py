from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store API keys in memory (in production, use proper database)
user_sessions = {}

class PrakritiAnalyzer:
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
            self.text_model = genai.GenerativeModel('gemini-1.5-pro')
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error = str(e)

    def analyze_plant_species(self, image_data, region):
        \"\"\"Analyze plant species using Gemini Vision\"\"\"
        try:
            # Convert base64 to image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            prompt = \"\"\"Analyze this plant image and provide structured information:
            1. Common Name 
            2. Scientific Name
            3. Family
            4. Key identifying characteristics
            5. Confidence level (High/Medium/Low)
            
            Format your response clearly.\"\"\"
            
            response = self.vision_model.generate_content([prompt, image])
            return {\"success\": True, \"analysis\": response.text}
        except Exception as e:
            return {\"success\": False, \"error\": f\"Vision analysis failed: {str(e)}\"}

    def get_climate_analysis(self, plant_info, region):
        \"\"\"Get climate expert analysis\"\"\"
        try:
            region_data = self.get_region_data(region)
            prompt = f\"\"\"Act as a climate expert analyzing plant compatibility:

Plant Analysis: {plant_info}
Region: {region}
Climate Data: {region_data}

Provide detailed climate compatibility assessment with:
- Overall compatibility rating
- Seasonal recommendations  
- Specific risks and opportunities
- Regional adaptation strategies\"\"\"

            response = self.text_model.generate_content(prompt)
            return {\"success\": True, \"analysis\": response.text}
        except Exception as e:
            return {\"success\": False, \"error\": f\"Climate analysis failed: {str(e)}\"}

    def get_biodiversity_analysis(self, plant_info, region):
        \"\"\"Get biodiversity expert analysis\"\"\"
        try:
            region_data = self.get_region_data(region)
            prompt = f\"\"\"Act as a biodiversity expert:

Plant Analysis: {plant_info} 
Region: {region}
Biodiversity Level: {region_data.get('biodiversity', 'Unknown')}

Provide ecological impact assessment with:
- Biodiversity enhancement potential
- Companion planting suggestions
- Conservation recommendations
- Ecosystem integration strategies\"\"\"

            response = self.text_model.generate_content(prompt)
            return {\"success\": True, \"analysis\": response.text}
        except Exception as e:
            return {\"success\": False, \"error\": f\"Biodiversity analysis failed: {str(e)}\"}

    def get_restoration_analysis(self, plant_info, region):
        \"\"\"Get restoration expert analysis\"\"\"
        try:
            prompt = f\"\"\"Act as an ecological restoration expert:

Plant Analysis: {plant_info}
Region: {region}

Develop comprehensive restoration plan with:
- Implementation timeline (phased approach)
- Expected ecological outcomes
- Community engagement strategies
- Monitoring and evaluation framework\"\"\"

            response = self.text_model.generate_content(prompt)
            return {\"success\": True, \"analysis\": response.text}
        except Exception as e:
            return {\"success\": False, \"error\": f\"Restoration analysis failed: {str(e)}\"}

    def get_region_data(self, region):
        \"\"\"Get regional climate and soil data\"\"\"
        region_data = {
            \"Maharashtra\": {\"climate\": \"Tropical\", \"temperature\": \"22-34°C\", \"rainfall\": \"700-1200mm\", \"soil_types\": [\"Black Soil\", \"Laterite Soil\"], \"soil_ph\": \"6.5-8.5\", \"biodiversity\": \"Medium-High\"},
            \"Karnataka\": {\"climate\": \"Tropical\", \"temperature\": \"20-35°C\", \"rainfall\": \"800-1400mm\", \"soil_types\": [\"Red Soil\", \"Black Soil\"], \"soil_ph\": \"6.0-8.0\", \"biodiversity\": \"High\"},
            \"Madhya Pradesh\": {\"climate\": \"Subtropical\", \"temperature\": \"18-38°C\", \"rainfall\": \"1000-1600mm\", \"soil_types\": [\"Black Soil\", \"Alluvial Soil\"], \"soil_ph\": \"6.5-8.5\", \"biodiversity\": \"High\"},
            \"Jharkhand\": {\"climate\": \"Subtropical\", \"temperature\": \"20-35°C\", \"rainfall\": \"1200-1600mm\", \"soil_types\": [\"Red Soil\", \"Laterite Soil\"], \"soil_ph\": \"5.5-7.5\", \"biodiversity\": \"High\"},
            \"Uttarakhand\": {\"climate\": \"Temperate\", \"temperature\": \"5-25°C\", \"rainfall\": \"1500-2500mm\", \"soil_types\": [\"Mountain Soil\", \"Forest Soil\"], \"soil_ph\": \"5.0-7.0\", \"biodiversity\": \"Very High\"},
            \"Rajasthan\": {\"climate\": \"Arid\", \"temperature\": \"25-45°C\", \"rainfall\": \"200-400mm\", \"soil_types\": [\"Desert Soil\", \"Sand Dunes\"], \"soil_ph\": \"7.5-9.0\", \"biodiversity\": \"Low-Medium\"},
            \"Kerala\": {\"climate\": \"Tropical\", \"temperature\": \"23-32°C\", \"rainfall\": \"3000-5000mm\", \"soil_types\": [\"Laterite Soil\", \"Alluvial Soil\"], \"soil_ph\": \"5.0-6.5\", \"biodiversity\": \"Very High\"}
        }
        return region_data.get(region, {})

@app.route('/')
def home():
    return jsonify({\"message\": \"Project Prakriti API is running\", \"status\": \"healthy\"})

@app.route('/analyze', methods=['POST'])
def analyze_plant():
    try:
        data = request.json
        api_key = data.get('api_key')
        image_data = data.get('image_data')
        region = data.get('region')
        
        if not api_key:
            return jsonify({\"success\": False, \"error\": \"API key is required\"})
        
        # Create analyzer with user's API key
        analyzer = PrakritiAnalyzer(api_key)
        if not analyzer.valid:
            return jsonify({\"success\": False, \"error\": f\"Invalid API key: {analyzer.error}\"})
        
        # Step 1: Species Identification
        species_result = analyzer.analyze_plant_species(image_data, region)
        if not species_result['success']:
            return jsonify({\"success\": False, \"error\": species_result['error']})
        
        # Step 2: Expert Analyses
        climate_result = analyzer.get_climate_analysis(species_result['analysis'], region)
        biodiversity_result = analyzer.get_biodiversity_analysis(species_result['analysis'], region)  
        restoration_result = analyzer.get_restoration_analysis(species_result['analysis'], region)
        
        # Get regional data
        region_info = analyzer.get_region_data(region)
        
        return jsonify({
            \"success\": True,
            \"species_analysis\": species_result['analysis'],
            \"climate_analysis\": climate_result['analysis'] if climate_result['success'] else climate_result['error'],
            \"biodiversity_analysis\": biodiversity_result['analysis'] if biodiversity_result['success'] else biodiversity_result['error'],
            \"restoration_analysis\": restoration_result['analysis'] if restoration_result['success'] else restoration_result['error'],
            \"region_data\": region_info
        })
        
    except Exception as e:
        return jsonify({\"success\": False, \"error\": f\"Analysis failed: {str(e)}\"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
