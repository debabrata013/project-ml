#!/usr/bin/env python3
"""
Comprehensive test script for enhanced Agriculture Assistant with Groq AI
"""

import os
import sys
import json
sys.path.append('.')

def test_groq_integration():
    """Test all Groq-powered AI features"""
    print("🚀 Testing Enhanced Agriculture Assistant with Groq AI")
    print("=" * 70)
    
    try:
        from tools import (
            analyze_crop_health_with_ai,
            generate_farming_plan,
            pest_disease_advisor,
            soil_analysis_advisor,
            market_price_advisor,
            weather_farming_advisor,
            predict_plant_disease,
            predict_crop_yield
        )
        
        # Test 1: Crop Health Analysis
        print("\n🌱 Testing AI Crop Health Analysis:")
        crop_data = json.dumps({
            "crop": "tomato",
            "growth_stage": "flowering",
            "symptoms": "yellowing leaves, stunted growth",
            "weather": "high humidity, moderate temperature",
            "soil_ph": 6.5
        })
        
        result = analyze_crop_health_with_ai(crop_data)
        if result.get("success"):
            print("✅ Crop health analysis completed")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 2: Farming Plan Generation
        print("\n📋 Testing Farming Plan Generation:")
        requirements = "10 acre farm, rice cultivation, monsoon season, budget 50000 INR"
        
        result = generate_farming_plan(requirements)
        if result.get("success"):
            print("✅ Farming plan generated")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 3: Pest & Disease Advisor
        print("\n🐛 Testing Pest & Disease Advisor:")
        symptoms = "white powdery substance on leaves, leaf curling, reduced growth"
        
        result = pest_disease_advisor(symptoms)
        if result.get("success"):
            print("✅ Pest/disease diagnosis completed")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 4: Soil Analysis
        print("\n🌍 Testing Soil Analysis Advisor:")
        soil_data = "pH: 7.2, Nitrogen: low, Phosphorus: medium, Potassium: high, Organic matter: 2.5%"
        
        result = soil_analysis_advisor(soil_data)
        if result.get("success"):
            print("✅ Soil analysis completed")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 5: Market Price Advisor
        print("\n💰 Testing Market Price Advisor:")
        crop_query = "wheat price trends Maharashtra"
        
        result = market_price_advisor(crop_query)
        if result.get("success"):
            print("✅ Market analysis completed")
            print(f"Data sources: {result['data_sources']}")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 6: Weather Farming Advisor
        print("\n🌦️ Testing Weather Farming Advisor:")
        weather_data = json.dumps({
            "current": {"temp": 28, "humidity": 75, "rainfall": 0},
            "forecast": {"next_7_days": "moderate rain expected"}
        })
        
        result = weather_farming_advisor(weather_data)
        if result.get("success"):
            print("✅ Weather farming advice generated")
            print(f"Model: {result['model']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 7: ML Models (existing)
        print("\n🤖 Testing ML Models:")
        
        # Plant disease detection
        test_image_dir = "../dataset/Plant Diseases Dataset/test/test"
        if os.path.exists(test_image_dir):
            test_images = [f for f in os.listdir(test_image_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:1]
            
            if test_images:
                test_image_path = os.path.join(test_image_dir, test_images[0])
                result = predict_plant_disease(test_image_path)
                if result.get("success"):
                    print(f"✅ Disease detected: {result['predicted_disease']}")
                    print(f"✅ Confidence: {result['confidence']:.3f}")
                else:
                    print(f"❌ Disease detection error: {result.get('error')}")
        
        # Crop yield prediction
        sample_data = '{"crop": "rice", "area": 10, "season": "kharif", "rainfall": 1200}'
        result = predict_crop_yield(sample_data)
        if result.get("success"):
            print(f"✅ Predicted yield: {result['predicted_yield']:.2f}")
        else:
            print(f"❌ Yield prediction error: {result.get('error')}")
        
        print(f"\n🎉 Enhanced Agriculture Assistant test completed!")
        print("=" * 70)
        print("🚀 Your agent now has SUPER POWERS:")
        print("   • Groq AI-powered expert consultation")
        print("   • Advanced crop health analysis")
        print("   • Comprehensive farming plans")
        print("   • Expert pest & disease diagnosis")
        print("   • Scientific soil analysis")
        print("   • Market intelligence & pricing")
        print("   • Weather-integrated recommendations")
        print("   • ML-based disease detection")
        print("   • AI-powered yield prediction")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install missing dependencies: pip install groq")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_groq_integration()
