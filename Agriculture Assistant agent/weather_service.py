import requests
import json

def get_weather_data(lat, lon):
    """Get weather data with fallback options"""
    try:
        # Try free weather service
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 7,
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            # Current weather
            current_weather = {
                "coord": {"lat": lat, "lon": lon},
                "weather": [{"description": "current conditions"}],
                "main": {
                    "temp": current.get("temperature_2m", 25),
                    "humidity": current.get("relative_humidity_2m", 60),
                    "pressure": 1013
                },
                "wind": {"speed": current.get("wind_speed_10m", 5)},
                "name": f"Location {lat},{lon}"
            }
            
            # Forecast
            forecast_data = {
                "list": [],
                "city": {"name": f"Location {lat},{lon}"}
            }
            
            for i in range(min(7, len(daily.get("time", [])))):
                forecast_data["list"].append({
                    "dt_txt": daily["time"][i],
                    "main": {
                        "temp_max": daily.get("temperature_2m_max", [25])[i],
                        "temp_min": daily.get("temperature_2m_min", [20])[i]
                    },
                    "weather": [{"description": "forecast"}]
                })
            
            return {
                "current": current_weather,
                "forecast": forecast_data,
                "source": "open-meteo"
            }
    except:
        pass
    
    # Fallback to location-based estimates
    # India climate estimates based on latitude
    if 8 <= lat <= 37:  # India latitude range
        temp = 28 if 15 <= lat <= 30 else 32  # Cooler in north, hotter in south
        humidity = 70 if lat < 20 else 60  # More humid in south
    else:
        temp = 25
        humidity = 65
    
    mock_current = {
        "coord": {"lat": lat, "lon": lon},
        "weather": [{"description": "partly cloudy"}],
        "main": {
            "temp": temp,
            "humidity": humidity,
            "pressure": 1013
        },
        "wind": {"speed": 3.5},
        "name": f"Location {lat},{lon}"
    }
    
    mock_forecast = {
        "list": [
            {
                "dt_txt": f"2024-01-0{i+1} 12:00:00",
                "main": {"temp_max": temp + 2, "temp_min": temp - 5},
                "weather": [{"description": "partly cloudy"}]
            } for i in range(7)
        ],
        "city": {"name": f"Location {lat},{lon}"}
    }
    
    return {
        "current": mock_current,
        "forecast": mock_forecast,
        "source": "estimated"
    }
