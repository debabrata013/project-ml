import os
import sys
import json
import requests
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_current_location():
    """Get current location using IP geolocation"""
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        return {
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "city": data.get("city"),
            "country": data.get("country")
        }
    except Exception as e:
        return {"error": f"Failed to get location: {str(e)}"}

def get_weather_forecast(input: str) -> dict:
    """Get 5-day weather forecast for current location or specified coordinates"""
    try:
        if input and input.strip():
            input_dict = json.loads(input)
            lat = input_dict.get("latitude")
            lon = input_dict.get("longitude")
        else:
            location = get_current_location()
            if "error" in location:
                return location
            lat = location["latitude"]
            lon = location["longitude"]
        
        url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
        
        querystring = {
            "latitude": str(lat),
            "longitude": str(lon),
            "lang": "EN"
        }
        
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "success": True,
                "location": {"latitude": lat, "longitude": lon},
                "forecast": weather_data
            }
        else:
            return {"error": f"API request failed: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

def get_current_weather(input: str) -> dict:
    """Get current weather for location"""
    try:
        if input and input.strip():
            input_dict = json.loads(input)
            lat = input_dict.get("latitude")
            lon = input_dict.get("longitude")
        else:
            location = get_current_location()
            if "error" in location:
                return location
            lat = location["latitude"]
            lon = location["longitude"]
        
        url = "https://open-weather13.p.rapidapi.com/city/latlon"
        
        querystring = {
            "lat": str(lat),
            "lon": str(lon)
        }
        
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "success": True,
                "location": {"latitude": lat, "longitude": lon},
                "current_weather": weather_data
            }
        else:
            return {"error": f"API request failed: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Failed to fetch current weather: {str(e)}"}

def search_agricultural_info(query: str) -> dict:
    """Search for agricultural information on the internet"""
    try:
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": f"{query} agriculture farming",
            "num": 5
        })
        
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            search_results = response.json()
            return {
                "success": True,
                "query": query,
                "results": search_results.get("organic", [])
            }
        else:
            return {"error": f"Search API request failed: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Failed to search: {str(e)}"}

def predict_plant_disease(image_path: str) -> dict:
    """Predict plant disease from image using trained CNN model"""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        model_path = os.path.join(models_dir, 'plant_disease_model.h5')
        classes_path = os.path.join(models_dir, 'plant_disease_classes.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(classes_path):
            return {"error": "Plant disease model files not found"}
        
        # Load model and classes
        model = tf.keras.models.load_model(model_path)
        class_names = joblib.load(classes_path)
        
        # Load and preprocess image
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        
        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        
        predicted_class = class_names[predicted_class_idx]
        
        # Get top 3 predictions
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = [(class_names[i], float(predictions[0][i])) for i in top_indices]
        
        return {
            "success": True,
            "predicted_disease": predicted_class,
            "confidence": float(confidence),
            "top_predictions": top_predictions,
            "recommendation": get_disease_treatment_advice(predicted_class)
        }
        
    except Exception as e:
        return {"error": f"Failed to predict plant disease: {str(e)}"}

def predict_crop_yield(input_data: str) -> dict:
    """Predict crop yield using trained ML model"""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Try multi-crop model first
        multi_model_path = os.path.join(models_dir, 'multi_crop_yield_model.pkl')
        encoders_path = os.path.join(models_dir, 'multi_crop_label_encoders.pkl')
        features_path = os.path.join(models_dir, 'multi_crop_feature_names.pkl')
        
        if os.path.exists(multi_model_path):
            model = joblib.load(multi_model_path)
            encoders = joblib.load(encoders_path)
            feature_names = joblib.load(features_path)
            
            # Parse input data
            data = json.loads(input_data)
            
            # Create feature array
            features = []
            for feature in feature_names:
                if feature in data:
                    if feature in encoders:
                        features.append(encoders[feature].transform([data[feature]])[0])
                    else:
                        features.append(float(data[feature]))
                else:
                    features.append(0)
            
            prediction = model.predict([features])[0]
            
            return {
                "success": True,
                "predicted_yield": float(prediction),
                "input_features": data,
                "model_type": "multi_crop"
            }
        else:
            return {"error": "Yield prediction model not found"}
            
    except Exception as e:
        return {"error": f"Failed to predict crop yield: {str(e)}"}

def get_disease_treatment_advice(disease_name: str) -> str:
    """Get treatment advice for detected plant disease"""
    treatments = {
        "healthy": "Plant appears healthy. Continue regular care and monitoring.",
        "blight": "Apply copper-based fungicide. Improve air circulation and avoid overhead watering.",
        "rust": "Use fungicide spray. Remove affected leaves and ensure proper spacing.",
        "spot": "Apply appropriate fungicide. Avoid watering leaves directly.",
        "wilt": "Check soil drainage. May need fungicide treatment and proper irrigation.",
        "mosaic": "Remove infected plants. Control aphids and use virus-free seeds.",
        "scab": "Apply fungicide during wet conditions. Improve air circulation."
    }
    
    disease_lower = disease_name.lower()
    for key, treatment in treatments.items():
        if key in disease_lower:
            return treatment
    
    return "Consult local agricultural extension office for specific treatment recommendations."

def analyze_crop_health_with_ai(crop_data: str) -> dict:
    """Advanced crop health analysis using Groq AI"""
    try:
        data = json.loads(crop_data)
        
        prompt = f"""
        As an expert agricultural AI, analyze this crop data and provide comprehensive insights:
        
        Crop Data: {json.dumps(data, indent=2)}
        
        Provide analysis on:
        1. Current crop health status
        2. Risk factors and potential issues
        3. Optimization recommendations
        4. Preventive measures
        5. Expected outcomes
        
        Format as JSON with clear recommendations.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        return {
            "success": True,
            "analysis": response.choices[0].message.content,
            "model": "llama-3.1-8b-instant"
        }
        
    except Exception as e:
        return {"error": f"Failed to analyze crop health: {str(e)}"}

def generate_farming_plan(requirements: str) -> dict:
    """Generate comprehensive farming plan using Groq AI"""
    try:
        prompt = f"""
        Create a detailed farming plan based on these requirements:
        {requirements}
        
        Include:
        1. Crop selection and rotation plan
        2. Timeline with monthly activities
        3. Resource requirements (seeds, fertilizers, water)
        4. Budget estimation
        5. Risk management strategies
        6. Expected yield and profit projections
        
        Provide practical, actionable plan in JSON format.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.4
        )
        
        return {
            "success": True,
            "farming_plan": response.choices[0].message.content,
            "model": "llama-3.1-8b-instant"
        }
        
    except Exception as e:
        return {"error": f"Failed to generate farming plan: {str(e)}"}

def pest_disease_advisor(symptoms: str) -> dict:
    """Advanced pest and disease identification and treatment using Groq AI"""
    try:
        prompt = f"""
        As an expert plant pathologist and entomologist, analyze these symptoms:
        
        Symptoms: {symptoms}
        
        Provide:
        1. Most likely pest/disease identification
        2. Confidence level (1-10)
        3. Detailed treatment protocol
        4. Organic and chemical treatment options
        5. Prevention strategies
        6. Timeline for recovery
        7. When to seek professional help
        
        Format as detailed JSON response.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.2
        )
        
        return {
            "success": True,
            "diagnosis": response.choices[0].message.content,
            "model": "llama-3.1-8b-instant"
        }
        
    except Exception as e:
        return {"error": f"Failed to diagnose pest/disease: {str(e)}"}

def soil_analysis_advisor(soil_data: str) -> dict:
    """Comprehensive soil analysis and recommendations using Groq AI"""
    try:
        prompt = f"""
        As a soil scientist, analyze this soil data and provide expert recommendations:
        
        Soil Data: {soil_data}
        
        Analyze and recommend:
        1. Soil health assessment
        2. Nutrient deficiencies/excesses
        3. pH adjustment strategies
        4. Organic matter improvement
        5. Suitable crops for this soil
        6. Fertilization schedule
        7. Soil conservation practices
        
        Provide detailed JSON response with actionable steps.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        return {
            "success": True,
            "soil_analysis": response.choices[0].message.content,
            "model": "llama-3.1-8b-instant"
        }
        
    except Exception as e:
        return {"error": f"Failed to analyze soil: {str(e)}"}

def market_price_advisor(crop_query: str) -> dict:
    """Get market insights and price predictions using AI analysis"""
    try:
        # First get current market data
        search_results = search_agricultural_info(f"{crop_query} market price trends India")
        
        if search_results.get("success"):
            market_data = search_results.get("results", [])
            
            prompt = f"""
            Analyze this market data for {crop_query} and provide insights:
            
            Market Data: {json.dumps(market_data[:3], indent=2)}
            
            Provide:
            1. Current price trends
            2. Price predictions for next 3-6 months
            3. Best selling strategies
            4. Market demand analysis
            5. Optimal harvest timing for maximum profit
            6. Alternative markets/buyers
            
            Format as actionable JSON response.
            """
            
            response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.4
            )
            
            return {
                "success": True,
                "market_analysis": response.choices[0].message.content,
                "data_sources": len(market_data),
                "model": "llama-3.1-8b-instant"
            }
        else:
            return {"error": "Failed to fetch market data"}
            
    except Exception as e:
        return {"error": f"Failed to analyze market: {str(e)}"}

def weather_farming_advisor(location_weather: str) -> dict:
    """Advanced weather-based farming recommendations using Groq AI"""
    try:
        prompt = f"""
        As a meteorological farming expert, analyze this weather data and provide farming advice:
        
        Weather Data: {location_weather}
        
        Provide recommendations for:
        1. Immediate farming activities (next 7 days)
        2. Crop protection strategies
        3. Irrigation scheduling
        4. Pest/disease risk assessment
        5. Harvesting recommendations
        6. Field preparation activities
        7. Emergency preparedness
        
        Format as detailed JSON with specific actions and timelines.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        return {
            "success": True,
            "weather_advice": response.choices[0].message.content,
            "model": "llama-3.1-8b-instant"
        }
        
    except Exception as e:
        return {"error": f"Failed to generate weather advice: {str(e)}"}

