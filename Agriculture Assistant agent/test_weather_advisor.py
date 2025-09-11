#!/usr/bin/env python3
"""
Test script for enhanced weather-based farming advisor
"""

import os
import sys
sys.path.append('.')

def test_weather_advisor():
    """Test the enhanced weather-based farming advisor"""
    print("🌤️ Testing Enhanced Weather-based Farming Advisor")
    print("=" * 70)
    
    try:
        from tools import weather_farming_advisor
        
        print("\n1. 📍 Getting Location and Weather Data...")
        result = weather_farming_advisor()
        
        if result.get("success"):
            print("✅ Successfully retrieved data and generated recommendations")
            
            # Location info
            location = result.get("location", {})
            print(f"\n📍 Location Detected:")
            print(f"   City: {location.get('city', 'Unknown')}")
            print(f"   Country: {location.get('country', 'Unknown')}")
            print(f"   Coordinates: {location.get('coordinates', {})}")
            
            # Weather summary
            weather = result.get("weather_summary", {})
            current = weather.get("current", {})
            print(f"\n🌤️ Current Weather:")
            print(f"   Temperature: {current.get('temp', 'N/A')}°C")
            print(f"   Conditions: {current.get('weather', [{}])[0].get('description', 'N/A') if current.get('weather') else 'N/A'}")
            
            # Farming recommendations
            recommendations = result.get("farming_recommendations", {})
            print(f"\n🚜 Farming Recommendations:")
            
            if isinstance(recommendations, dict):
                # Immediate activities
                activities = recommendations.get("immediate_activities", [])
                if activities:
                    print(f"\n   Immediate Activities:")
                    for activity in activities[:3]:
                        print(f"   - {activity}")
                
                # Protection strategies
                protection = recommendations.get("crop_protection", [])
                if protection:
                    print(f"\n   Protection Strategies:")
                    for strategy in protection[:2]:
                        print(f"   - {strategy}")
                
                # Irrigation recommendations
                irrigation = recommendations.get("irrigation", [])
                if irrigation:
                    print(f"\n   Irrigation Recommendations:")
                    for rec in irrigation[:2]:
                        print(f"   - {rec}")
                
                # Risk assessment
                risks = recommendations.get("pest_disease_risk", [])
                if risks:
                    print(f"\n   Risk Assessment:")
                    for risk in risks[:2]:
                        print(f"   - {risk}")
            else:
                print("   Raw AI Recommendations:", recommendations)
            
            print(f"\n⏰ Data Timestamp: {result.get('data_timestamp', 'N/A')}")
            
        else:
            print(f"❌ Error: {result.get('error')}")
        
        print(f"\n🎉 Weather Advisor Test Completed!")
        print("=" * 70)
        print("🚀 New Capabilities:")
        print("   • Automatic location detection")
        print("   • Real-time weather data")
        print("   • 7-day weather forecast")
        print("   • AI-powered farming recommendations")
        print("   • Location-specific advice")
        print("   • Risk assessment and alerts")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_weather_advisor()
