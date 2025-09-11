import requests
import json
import os
from datetime import datetime, timedelta

# Cache location data
LOCATION_CACHE_FILE = "location_cache.json"
CACHE_DURATION_HOURS = 24

def load_cached_location():
    """Load cached location if available and not expired"""
    try:
        if os.path.exists(LOCATION_CACHE_FILE):
            with open(LOCATION_CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid (24 hours)
            cache_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
            if datetime.now() - cache_time < timedelta(hours=CACHE_DURATION_HOURS):
                return cache_data.get('location')
    except:
        pass
    return None

def save_location_cache(location_data):
    """Save location data to cache"""
    try:
        cache_data = {
            'location': location_data,
            'timestamp': datetime.now().isoformat()
        }
        with open(LOCATION_CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except:
        pass

def get_location_multiple_sources():
    """Get location using multiple sources with fallbacks"""
    
    # Try cached location first
    cached_location = load_cached_location()
    if cached_location:
        return cached_location
    
    # Method 1: ip-api.com (most reliable)
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                location = {
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "city": data.get("city"),
                    "country": data.get("country"),
                    "state": data.get("regionName"),
                    "source": "ip-api"
                }
                save_location_cache(location)
                return location
    except:
        pass
    
    # Method 2: ipapi.co
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            location = {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "city": data.get("city"),
                "country": data.get("country_name"),
                "state": data.get("region"),
                "source": "ipapi"
            }
            save_location_cache(location)
            return location
    except:
        pass
    
    # Method 3: ipinfo.io
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc", "").split(",")
            if len(loc) == 2:
                location = {
                    "latitude": float(loc[0]),
                    "longitude": float(loc[1]),
                    "city": data.get("city"),
                    "country": data.get("country"),
                    "state": data.get("region"),
                    "source": "ipinfo"
                }
                save_location_cache(location)
                return location
    except:
        pass
    
    # Method 4: Default to major Indian city (Hyderabad) as fallback
    # This ensures the system always works
    default_location = {
        "latitude": 17.3932,
        "longitude": 78.4917,
        "city": "Hyderabad",
        "country": "India",
        "state": "Telangana",
        "source": "default_fallback",
        "note": "Using default location - Hyderabad, India"
    }
    
    save_location_cache(default_location)
    return default_location

def get_user_location_with_context():
    """Get location with additional context for better farming advice"""
    location = get_location_multiple_sources()
    
    # Add agricultural context based on location
    if location.get("country") == "India":
        # Add Indian agricultural context
        location["agricultural_context"] = {
            "climate_zone": get_indian_climate_zone(location.get("state", "")),
            "major_crops": get_major_crops_by_state(location.get("state", "")),
            "cropping_seasons": ["Kharif", "Rabi", "Zaid"],
            "monsoon_pattern": "Southwest and Northeast monsoons"
        }
    
    return location

def get_indian_climate_zone(state):
    """Get climate zone for Indian states"""
    climate_zones = {
        "Telangana": "Semi-arid",
        "Andhra Pradesh": "Tropical",
        "Karnataka": "Tropical/Semi-arid",
        "Tamil Nadu": "Tropical",
        "Kerala": "Tropical",
        "Maharashtra": "Tropical/Semi-arid",
        "Gujarat": "Arid/Semi-arid",
        "Rajasthan": "Arid/Semi-arid",
        "Punjab": "Sub-tropical",
        "Haryana": "Sub-tropical",
        "Uttar Pradesh": "Sub-tropical",
        "Bihar": "Sub-tropical",
        "West Bengal": "Tropical/Sub-tropical"
    }
    return climate_zones.get(state, "Tropical/Sub-tropical")

def get_major_crops_by_state(state):
    """Get major crops for Indian states"""
    state_crops = {
        "Telangana": ["Rice", "Cotton", "Maize", "Sugarcane"],
        "Andhra Pradesh": ["Rice", "Cotton", "Sugarcane", "Chili"],
        "Karnataka": ["Rice", "Cotton", "Sugarcane", "Coffee"],
        "Tamil Nadu": ["Rice", "Cotton", "Sugarcane", "Groundnut"],
        "Kerala": ["Rice", "Coconut", "Spices", "Rubber"],
        "Maharashtra": ["Cotton", "Sugarcane", "Soybean", "Wheat"],
        "Gujarat": ["Cotton", "Groundnut", "Wheat", "Sugarcane"],
        "Punjab": ["Wheat", "Rice", "Cotton", "Sugarcane"],
        "Haryana": ["Wheat", "Rice", "Cotton", "Mustard"],
        "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane", "Potato"]
    }
    return state_crops.get(state, ["Rice", "Wheat", "Cotton", "Sugarcane"])
