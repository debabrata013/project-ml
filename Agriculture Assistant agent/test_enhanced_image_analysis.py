#!/usr/bin/env python3
"""
Test script for enhanced plant disease detection with comprehensive image analysis
"""

import os
import sys
sys.path.append('.')

def test_enhanced_image_analysis():
    """Test the enhanced image analysis capabilities"""
    print("🔬 Testing Enhanced Plant Disease Detection with Image Analysis")
    print("=" * 70)
    
    try:
        from tools import predict_plant_disease
        from image_analysis_service import analyze_plant_image_comprehensive
        
        # Test image analysis service
        test_image_dir = "../dataset/Plant Diseases Dataset/test/test"
        if os.path.exists(test_image_dir):
            test_images = [f for f in os.listdir(test_image_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:1]
            
            if test_images:
                test_image_path = os.path.join(test_image_dir, test_images[0])
                print(f"\n🖼️ Testing Image: {test_images[0]}")
                
                # Test comprehensive image analysis
                print("\n1. 🔍 Comprehensive Image Analysis:")
                analysis_result = analyze_plant_image_comprehensive(test_image_path)
                
                if analysis_result.get("success"):
                    print("✅ Image analysis completed")
                    
                    # Display key findings
                    comp_assessment = analysis_result.get("comprehensive_assessment", {})
                    print(f"   Overall Health: {comp_assessment.get('overall_health', 'unknown')}")
                    print(f"   Severity Level: {comp_assessment.get('severity_level', 'unknown')}")
                    print(f"   Disease Indicators: {len(comp_assessment.get('disease_indicators', []))}")
                    
                    color_analysis = analysis_result.get("color_analysis", {})
                    print(f"   Color Analysis:")
                    for condition, data in color_analysis.items():
                        if data.get("percentage", 0) > 1:
                            print(f"     - {condition}: {data['percentage']:.1f}%")
                    
                    texture_analysis = analysis_result.get("texture_analysis", {})
                    print(f"   Texture Analysis:")
                    print(f"     - Spots detected: {texture_analysis.get('spot_count', 0)}")
                    print(f"     - Edge density: {texture_analysis.get('edge_density', 0):.3f}")
                else:
                    print(f"❌ Image analysis failed: {analysis_result.get('error')}")
                
                # Test enhanced disease prediction
                print("\n2. 🤖 Enhanced Disease Prediction:")
                prediction_result = predict_plant_disease(test_image_path)
                
                if prediction_result.get("success"):
                    print("✅ Enhanced prediction completed")
                    
                    ml_pred = prediction_result.get("ml_prediction", {})
                    print(f"   ML Prediction: {ml_pred.get('predicted_disease')}")
                    print(f"   ML Confidence: {ml_pred.get('confidence', 0):.3f}")
                    
                    detailed_assessment = prediction_result.get("detailed_assessment", {})
                    print(f"   Disease Confirmation: {detailed_assessment.get('disease_confirmation')}")
                    print(f"   Confidence Level: {detailed_assessment.get('confidence_level')}")
                    print(f"   Progression Stage: {detailed_assessment.get('progression_stage')}")
                    
                    key_symptoms = detailed_assessment.get("key_symptoms", [])
                    if key_symptoms:
                        print(f"   Key Symptoms:")
                        for symptom in key_symptoms[:3]:
                            print(f"     - {symptom}")
                    
                    treatment = prediction_result.get("treatment_recommendations", {})
                    immediate_actions = treatment.get("immediate_actions", [])
                    if immediate_actions:
                        print(f"   Immediate Actions:")
                        for action in immediate_actions[:2]:
                            print(f"     - {action}")
                else:
                    print(f"❌ Enhanced prediction failed: {prediction_result.get('error')}")
                
                print(f"\n🎉 Enhanced Image Analysis Test Completed!")
                print("=" * 70)
                print("🚀 New Capabilities:")
                print("   • Comprehensive color analysis for disease detection")
                print("   • Texture and pattern analysis for spot identification")
                print("   • AI-powered detailed symptom description")
                print("   • Severity assessment and progression staging")
                print("   • Enhanced treatment recommendations")
                print("   • Detailed monitoring schedules")
                
            else:
                print("⚠️  No test images found")
        else:
            print("⚠️  Test image directory not found")
            print("   You can test with any plant image by providing the path")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install missing dependencies: pip install opencv-python")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_enhanced_image_analysis()
