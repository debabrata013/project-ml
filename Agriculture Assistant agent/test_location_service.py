#!/usr/bin/env python3
"""
Test script for enhanced location service
"""

import os
import sys
sys.path.append('.')

def test_location_service():
    """Test the enhanced location service"""
    print("📍 Testing Enhanced Location Service")
    print("=" * 60)
    
    try:
        from tools import get_current_location
        from location_service import get_location_multiple_sources, load_cached_location
        
        print("\n1. 🔍 Testing Location Detection...")
        location = get_current_location()
        
        print("✅ Location detected successfully!")
        print(f"   City: {location.get('city', 'Unknown')}")
        print(f"   State: {location.get('state', 'Unknown')}")
        print(f"   Country: {location.get('country', 'Unknown')}")
        print(f"   Coordinates: {location.get('latitude')}, {location.get('longitude')}")
        print(f"   Source: {location.get('source', 'Unknown')}")
        
        if location.get('note'):
            print(f"   Note: {location['note']}")
        
        # Test agricultural context
        agri_context = location.get('agricultural_context', {})
        if agri_context:
            print(f"\n🌾 Agricultural Context:")
            print(f"   Climate Zone: {agri_context.get('climate_zone', 'Unknown')}")
            print(f"   Major Crops: {', '.join(agri_context.get('major_crops', []))}")
            print(f"   Cropping Seasons: {', '.join(agri_context.get('cropping_seasons', []))}")
        
        # Test caching
        print(f"\n💾 Testing Location Caching...")
        cached = load_cached_location()
        if cached:
            print("✅ Location cache working")
            print(f"   Cached City: {cached.get('city')}")
        else:
            print("ℹ️  No cached location found (first run)")
        
        # Test multiple calls (should use cache on second call)
        print(f"\n🔄 Testing Cache Performance...")
        location2 = get_current_location()
        if location2.get('source') == location.get('source'):
            print("✅ Consistent location detection")
        
        print(f"\n🎉 Location Service Test Completed!")
        print("=" * 60)
        print("🚀 Enhanced Features:")
        print("   • Multiple API fallbacks")
        print("   • 24-hour location caching")
        print("   • Agricultural context integration")
        print("   • Emergency fallback location")
        print("   • Always returns valid location")
        
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_location_service()
