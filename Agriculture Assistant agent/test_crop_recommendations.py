#!/usr/bin/env python3
"""
Test script for automatic crop recommendation system
"""

import os
import sys
sys.path.append('.')

def test_crop_recommendations():
    """Test the automatic crop recommendation system"""
    print("🌾 Testing Automatic Crop Recommendation System")
    print("=" * 70)
    
    try:
        from tools import recommend_suitable_crops
        
        print("\n1. 📍 Analyzing Location and Conditions...")
        result = recommend_suitable_crops(5)  # 5 acres
        
        if result.get("success"):
            print("✅ Successfully generated recommendations")
            
            # Location info
            location = result.get("location_details", {})
            print(f"\n📍 Location Analysis:")
            print(f"   City: {location.get('city', 'Unknown')}")
            print(f"   Country: {location.get('country', 'Unknown')}")
            print(f"   Coordinates: {location.get('coordinates', {})}")
            
            # Farm profile
            farm = result.get("farm_profile", {})
            print(f"\n🚜 Farm Profile:")
            print(f"   Size: {farm.get('size_acres', 0)} acres")
            
            advantages = farm.get("location_advantages", [])
            if advantages:
                print("   Location Advantages:")
                for adv in advantages[:2]:
                    print(f"   - {adv}")
            
            challenges = farm.get("potential_challenges", [])
            if challenges:
                print("   Potential Challenges:")
                for chl in challenges[:2]:
                    print(f"   - {chl}")
            
            # Crop recommendations
            recommendations = result.get("crop_recommendations", {})
            crops = recommendations.get("recommended_crops", [])
            if crops:
                print(f"\n🌱 Top Recommended Crops:")
                for crop in crops[:3]:
                    print(f"\n   {crop.get('name', 'Unknown Crop')}:")
                    print(f"   - Reason: {crop.get('reason', 'N/A')}")
                    print(f"   - Season: {crop.get('planting_season', 'N/A')}")
                    print(f"   - Water Needs: {crop.get('water_requirements', 'N/A')}")
                    print(f"   - Expected Yield: {crop.get('expected_yield', 'N/A')}")
            
            # Market insights
            market = result.get("market_insights", {})
            if market:
                print(f"\n💰 Market Analysis:")
                for crop, analysis in market.items():
                    print(f"\n   {crop}:")
                    if isinstance(analysis, dict):
                        if "current_price" in analysis:
                            print(f"   - Current Price: {analysis['current_price']}")
                        if "trend" in analysis:
                            print(f"   - Market Trend: {analysis['trend']}")
                    else:
                        print(f"   - Analysis: {analysis}")
            
            print(f"\n⏰ Data Timestamp: {result.get('data_timestamp', 'N/A')}")
            print(f"📊 Confidence Score: {result.get('confidence_score', 'N/A')}")
            
            # Data sources
            sources = result.get("data_sources", [])
            if sources:
                print(f"\n📚 Data Sources Used:")
                for source in sources:
                    print(f"   • {source}")
            
        else:
            print(f"❌ Error: {result.get('error')}")
        
        print(f"\n🎉 Crop Recommendation Test Completed!")
        print("=" * 70)
        print("🚀 System Capabilities:")
        print("   • Automatic location analysis")
        print("   • Climate pattern assessment")
        print("   • Local agriculture insights")
        print("   • Market demand analysis")
        print("   • Crop-specific recommendations")
        print("   • Economic viability assessment")
        print("   • Risk analysis and mitigation")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_crop_recommendations()
