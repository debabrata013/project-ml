import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

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

