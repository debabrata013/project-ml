#!/usr/bin/env python3
"""
Test script for enhanced Agriculture Assistant with ML capabilities
"""

import os
import sys
sys.path.append('.')

def test_ml_integration():
    """Test the ML model integration"""
    print("🧪 Testing Enhanced Agriculture Assistant ML Integration")
    print("=" * 60)
    
    try:
        from tools import predict_plant_disease, predict_crop_yield
        
        # Test plant disease prediction (if test images exist)
        test_image_dir = "../dataset/Plant Diseases Dataset/test/test"
        if os.path.exists(test_image_dir):
            test_images = [f for f in os.listdir(test_image_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:1]
            
            if test_images:
                test_image_path = os.path.join(test_image_dir, test_images[0])
                print(f"\n🌱 Testing Plant Disease Detection:")
                print(f"Image: {test_images[0]}")
                
                result = predict_plant_disease(test_image_path)
                if result.get("success"):
                    print(f"✅ Disease: {result['predicted_disease']}")
                    print(f"✅ Confidence: {result['confidence']:.3f}")
                    print(f"✅ Treatment: {result['recommendation']}")
                else:
                    print(f"❌ Error: {result.get('error')}")
            else:
                print("⚠️  No test images found")
        else:
            print("⚠️  Test image directory not found")
        
        # Test yield prediction
        print(f"\n🌾 Testing Crop Yield Prediction:")
        sample_data = '{"crop": "rice", "area": 10, "season": "kharif", "rainfall": 1200}'
        
        result = predict_crop_yield(sample_data)
        if result.get("success"):
            print(f"✅ Predicted Yield: {result['predicted_yield']:.2f}")
            print(f"✅ Model Type: {result['model_type']}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        print(f"\n✅ ML Integration test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_ml_integration()
