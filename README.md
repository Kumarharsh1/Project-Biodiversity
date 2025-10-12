# 🌿 Project Prakriti - Full Stack AI Plant Analysis

A full-stack application for plant species identification and ecological analysis using Google Gemini AI.

## 🚀 Features

- **Real AI Analysis**: Uses Gemini Vision AI for plant identification
- **Expert Analysis**: Climate, Biodiversity, and Restoration experts
- **Regional Data**: Specific analysis for Indian states
- **Secure API**: Backend handles API keys securely
- **Beautiful UI**: Streamlit frontend with professional design

## 🛠️ Setup Instructions

### Option 1: Local Development

1. **Start Backend** (Terminal 1):
   \\\powershell
   .\run_backend.ps1
   \\\

2. **Start Frontend** (Terminal 2):
   \\\powershell
   .\run_frontend.ps1
   \\\

3. **Access Application**:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:5000

### Option 2: Deploy to Heroku/Railway

1. **Backend Deployment**:
   - Deploy to Heroku/Railway using the Procfile
   - Set environment variables

2. **Frontend Deployment**:
   - Deploy to Streamlit Cloud
   - Update backend URL in app.py

## 🔑 API Configuration

1. Get FREE Gemini API key from: https://ai.google.dev/
2. Enter API key in the Streamlit sidebar
3. Upload plant image and select region
4. Get real AI analysis

## 📁 Project Structure

- \pp.py\ - Streamlit frontend
- \pi.py\ - Flask backend API  
- \equirements.txt\ - Python dependencies
- \Procfile\ - Backend deployment config
- \un_*.ps1\ - PowerShell setup scripts

## 🌍 Supported Regions

- Maharashtra, Karnataka, Madhya Pradesh
- Jharkhand, Uttarakhand, Rajasthan, Kerala

## 🔧 Troubleshooting

- **Backend Connection**: Ensure Flask server is running on port 5000
- **API Key**: Verify Gemini API key is valid
- **Image Upload**: Use clear, well-lit plant images
- **Dependencies**: Run \pip install -r requirements.txt\

## 📞 Support

For issues and questions, check the GitHub repository.
