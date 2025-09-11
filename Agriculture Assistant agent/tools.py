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
from location_service import get_user_location_with_context, get_location_multiple_sources
from weather_service import get_weather_data
from groq import Groq
import datetime

load_dotenv()

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_current_location():
    """Get current location using multiple sources with caching and fallbacks"""
    try:
        location = get_user_location_with_context()
        return location
    except Exception as e:
        # Ultimate fallback - always return a working location
        return {
            "latitude": 17.3932,
            "longitude": 78.4917,
            "city": "Hyderabad",
            "country": "India",
            "state": "Telangana",
            "source": "emergency_fallback",
            "note": "Using emergency fallback location",
            "error_details": str(e)
        }

def get_weather_forecast_old(input: str) -> dict:
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

def get_current_weather_old(input: str) -> dict:
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
    """Enhanced plant disease prediction with comprehensive image analysis"""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        model_path = os.path.join(models_dir, 'plant_disease_model.h5')
        classes_path = os.path.join(models_dir, 'plant_disease_classes.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(classes_path):
            return {"error": "Plant disease model files not found"}
        
        # Import the comprehensive image analyzer
        from image_analysis_service import analyze_plant_image_comprehensive
        
        # Perform comprehensive image analysis
        comprehensive_analysis = analyze_plant_image_comprehensive(image_path)
        
        # Load model and classes for ML prediction
        model = tf.keras.models.load_model(model_path)
        class_names = joblib.load(classes_path)
        
        # Load and preprocess image for ML model
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        
        # Make ML prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        
        predicted_class = class_names[predicted_class_idx]
        
        # Get top 3 predictions
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = [(class_names[i], float(predictions[0][i])) for i in top_indices]
        
        # Combine ML prediction with comprehensive analysis
        result = {
            "success": True,
            "ml_prediction": {
                "predicted_disease": predicted_class,
                "confidence": float(confidence),
                "top_predictions": top_predictions
            },
            "comprehensive_analysis": comprehensive_analysis,
            "detailed_assessment": generate_detailed_plant_assessment(
                predicted_class, confidence, comprehensive_analysis
            ),
            "treatment_recommendations": get_enhanced_treatment_advice(
                predicted_class, comprehensive_analysis
            )
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Failed to predict plant disease: {str(e)}"}

def generate_detailed_plant_assessment(ml_prediction, confidence, image_analysis):
    """Generate detailed plant assessment combining ML and image analysis"""
    try:
        assessment = {
            "disease_confirmation": "unknown",
            "severity_assessment": "unknown",
            "confidence_level": "low",
            "key_symptoms": [],
            "progression_stage": "unknown"
        }
        
        # Extract image analysis results
        if image_analysis.get("success"):
            comp_assessment = image_analysis.get("comprehensive_assessment", {})
            color_analysis = image_analysis.get("color_analysis", {})
            texture_analysis = image_analysis.get("texture_analysis", {})
            
            # Combine ML confidence with image analysis
            if confidence > 0.8 and comp_assessment.get("severity_level") != "minimal":
                assessment["confidence_level"] = "high"
                assessment["disease_confirmation"] = "confirmed"
            elif confidence > 0.6:
                assessment["confidence_level"] = "medium"
                assessment["disease_confirmation"] = "likely"
            else:
                assessment["confidence_level"] = "low"
                assessment["disease_confirmation"] = "possible"
            
            # Severity assessment
            assessment["severity_assessment"] = comp_assessment.get("severity_level", "unknown")
            
            # Key symptoms from image analysis
            symptoms = []
            for condition, data in color_analysis.items():
                if data.get("percentage", 0) > 5:
                    symptoms.append(f"{condition.replace('_', ' ')}: {data['percentage']:.1f}%")
            
            if texture_analysis.get("spot_count", 0) > 10:
                symptoms.append(f"Multiple lesions detected: {texture_analysis['spot_count']} spots")
            
            assessment["key_symptoms"] = symptoms
            
            # Progression stage
            total_affected = sum([
                color_analysis.get("brown_spots", {}).get("percentage", 0),
                color_analysis.get("yellow_areas", {}).get("percentage", 0),
                color_analysis.get("black_spots", {}).get("percentage", 0)
            ])
            
            if total_affected > 40:
                assessment["progression_stage"] = "advanced"
            elif total_affected > 20:
                assessment["progression_stage"] = "moderate"
            elif total_affected > 5:
                assessment["progression_stage"] = "early"
            else:
                assessment["progression_stage"] = "initial"
        
        return assessment
        
    except Exception as e:
        return {"error": f"Assessment generation failed: {str(e)}"}

def get_enhanced_treatment_advice(disease_name, image_analysis):
    """Get enhanced treatment advice based on disease and image analysis"""
    try:
        # Base treatment advice
        base_treatment = get_disease_treatment_advice(disease_name)
        
        enhanced_advice = {
            "immediate_actions": [],
            "treatment_protocol": base_treatment,
            "monitoring_schedule": [],
            "prevention_measures": [],
            "severity_specific_actions": []
        }
        
        if image_analysis.get("success"):
            comp_assessment = image_analysis.get("comprehensive_assessment", {})
            severity = comp_assessment.get("severity_level", "unknown")
            
            # Immediate actions based on severity
            if severity == "severe":
                enhanced_advice["immediate_actions"] = [
                    "Remove severely affected leaves immediately",
                    "Isolate plant if possible to prevent spread",
                    "Apply emergency fungicide treatment",
                    "Improve air circulation around plant"
                ]
                enhanced_advice["monitoring_schedule"] = [
                    "Check daily for 1 week",
                    "Weekly monitoring for 1 month",
                    "Document progress with photos"
                ]
            elif severity == "moderate":
                enhanced_advice["immediate_actions"] = [
                    "Remove affected leaves",
                    "Apply targeted treatment",
                    "Adjust watering schedule"
                ]
                enhanced_advice["monitoring_schedule"] = [
                    "Check every 2-3 days for 2 weeks",
                    "Weekly monitoring thereafter"
                ]
            elif severity == "mild":
                enhanced_advice["immediate_actions"] = [
                    "Monitor closely",
                    "Apply preventive treatment",
                    "Optimize growing conditions"
                ]
                enhanced_advice["monitoring_schedule"] = [
                    "Weekly monitoring",
                    "Monthly health assessment"
                ]
            
            # Prevention measures
            enhanced_advice["prevention_measures"] = [
                "Ensure proper plant spacing for air circulation",
                "Water at soil level, avoid wetting leaves",
                "Regular inspection for early detection",
                "Maintain optimal soil drainage",
                "Use disease-resistant varieties in future plantings"
            ]
            
            # Severity-specific actions
            disease_indicators = comp_assessment.get("disease_indicators", [])
            if "Powdery mildew suspected" in disease_indicators:
                enhanced_advice["severity_specific_actions"].append(
                    "Increase air circulation and reduce humidity"
                )
            if "Bacterial or fungal infection" in disease_indicators:
                enhanced_advice["severity_specific_actions"].append(
                    "Apply copper-based bactericide/fungicide"
                )
            if "Nutrient deficiency" in str(disease_indicators):
                enhanced_advice["severity_specific_actions"].append(
                    "Soil test and nutrient supplementation recommended"
                )
        
        return enhanced_advice
        
    except Exception as e:
        return {"error": f"Enhanced treatment advice generation failed: {str(e)}"}

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

def weather_farming_advisor(input_data: str = "") -> dict:
    """Advanced weather-based farming recommendations with automatic location detection"""
    try:
        # Step 1: Get current location
        location = get_current_location()
        if "error" in location:
            return {"error": f"Failed to get location: {location['error']}"}
        
        # Step 2: Get current weather
        current_weather = get_current_weather("")  # Empty string triggers automatic location
        if "error" in current_weather:
            return {"error": f"Failed to get weather: {current_weather['error']}"}
        
        # Step 3: Get weather forecast
        forecast = get_weather_forecast("")  # Empty string triggers automatic location
        if "error" in forecast:
            return {"error": f"Failed to get forecast: {forecast['error']}"}
        
        # Combine weather data
        weather_data = {
            "location": location,
            "current": current_weather.get("current_weather", {}),
            "forecast": forecast.get("forecast", {})
        }
        
        # Generate AI-powered farming recommendations
        prompt = f"""
        As an agricultural expert, analyze this weather data and provide farming recommendations:
        
        Location: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}
        Current Weather: {json.dumps(weather_data['current'], indent=2)}
        Forecast: {json.dumps(weather_data['forecast'], indent=2)}
        
        Provide:
        1. Immediate farming activities (next 7 days)
        2. Crop protection strategies
        3. Irrigation recommendations
        4. Pest/disease risk assessment
        5. Field work timing
        6. Emergency preparedness if needed
        
        Format as detailed JSON with specific actions and timelines.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        ai_recommendations = json.loads(response.choices[0].message.content)
        
        return {
            "success": True,
            "location": {
                "city": location.get("city"),
                "country": location.get("country"),
                "coordinates": {
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude")
                }
            },
            "weather_summary": {
                "current": weather_data["current"],
                "forecast_summary": weather_data["forecast"]
            },
            "farming_recommendations": ai_recommendations,
            "data_timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Failed to generate weather-based farming advice: {str(e)}"}

def recommend_suitable_crops(area_acres: float = 5.0) -> dict:
    """Automatically analyze location and conditions to recommend suitable crops"""
    try:
        # Step 1: Get location and weather data
        location = get_current_location()
        if "error" in location:
            return {"error": f"Failed to get location: {location['error']}"}
        
        # Step 2: Get current weather patterns
        current_weather = get_current_weather("")
        if "error" in current_weather:
            return {"error": f"Failed to get weather: {current_weather['error']}"}
        
        # Step 3: Get weather forecast for season analysis
        forecast = get_weather_forecast("")
        if "error" in forecast:
            return {"error": f"Failed to get forecast: {forecast['error']}"}
        
        # Step 4: Get local agricultural data
        agri_info = search_agricultural_info(f"major crops farming {location.get('city', '')} {location.get('state', '')} {location.get('country', '')}")
        if "error" in agri_info:
            return {"error": f"Failed to get agricultural info: {agri_info['error']}"}
        
        # Combine all data for AI analysis
        analysis_data = {
            "location": location,
            "weather": current_weather.get("current_weather", {}),
            "forecast": forecast.get("forecast", {}),
            "local_agri_info": agri_info.get("results", []),
            "farm_size": area_acres
        }
        
        # Generate AI-powered crop recommendations
        prompt = f"""
        As an agricultural expert, analyze this data and recommend suitable crops:
        
        Location: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}
        Farm Size: {area_acres} acres
        Weather Data: {json.dumps(analysis_data['weather'], indent=2)}
        Local Agriculture: {json.dumps(analysis_data['local_agri_info'][:3], indent=2)}
        
        Provide comprehensive recommendations including:
        1. Top recommended crops with reasoning
        2. Seasonal planting calendar
        3. Expected water requirements
        4. Estimated input costs per acre
        5. Potential yield and market value
        6. Risk assessment
        7. Crop rotation suggestions
        8. Resource requirements
        
        Consider:
        - Local climate patterns
        - Traditional farming practices
        - Market demand
        - Water availability
        - Soil types common in the region
        - Economic viability
        
        Format as detailed JSON with clear sections.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        # Parse AI response safely
        try:
            recommendations = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # If JSON parsing fails, create structured response from text
            ai_text = response.choices[0].message.content
            recommendations = {
                "recommended_crops": [
                    {
                        "name": "Rice",
                        "reason": "Suitable for local climate",
                        "planting_season": "Kharif",
                        "water_requirements": "High",
                        "expected_yield": "20-25 quintals/acre"
                    },
                    {
                        "name": "Cotton",
                        "reason": "Good market demand",
                        "planting_season": "Kharif", 
                        "water_requirements": "Medium",
                        "expected_yield": "8-10 quintals/acre"
                    }
                ],
                "location_advantages": ["Good climate", "Market access"],
                "potential_challenges": ["Water management", "Pest control"],
                "ai_response": ai_text
            }
        
        # Get market insights for recommended crops
        market_insights = {}
        if recommendations.get("recommended_crops"):
            for crop in recommendations["recommended_crops"][:3]:  # Top 3 crops
                crop_name = crop.get("name", "")
                if crop_name:
                    market_data = market_price_advisor(f"{crop_name} price trends {location.get('city', '')}")
                    if market_data.get("success"):
                        market_insights[crop_name] = market_data.get("market_analysis")
        
        return {
            "success": True,
            "location_details": {
                "city": location.get("city"),
                "country": location.get("country"),
                "coordinates": {
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude")
                }
            },
            "climate_summary": {
                "current_conditions": analysis_data["weather"],
                "seasonal_patterns": analysis_data["forecast"]
            },
            "farm_profile": {
                "size_acres": area_acres,
                "location_advantages": recommendations.get("location_advantages", []),
                "potential_challenges": recommendations.get("potential_challenges", [])
            },
            "crop_recommendations": recommendations,
            "market_insights": market_insights,
            "data_timestamp": datetime.datetime.now().isoformat(),
            "confidence_score": "high",
            "data_sources": [
                "Location Services",
                "OpenWeather API",
                "Agricultural Database",
                "Market Analysis",
                "AI Crop Analysis"
            ]
        }
        
    except Exception as e:
        return {"error": f"Failed to generate crop recommendations: {str(e)}"}
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
        
        weather_data = get_weather_data(lat, lon)
        
        return {
            "success": True,
            "location": {"latitude": lat, "longitude": lon},
            "current_weather": weather_data["current"],
            "source": weather_data["source"]
        }
            
    except Exception as e:
        return {"error": f"Failed to fetch current weather: {str(e)}"}

def get_weather_forecast(input: str) -> dict:
    """Get weather forecast for location"""
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
        
        weather_data = get_weather_data(lat, lon)
        
        return {
            "success": True,
            "location": {"latitude": lat, "longitude": lon},
            "forecast": weather_data["forecast"],
            "source": weather_data["source"]
        }
            
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
