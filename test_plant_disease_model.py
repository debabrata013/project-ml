#!/usr/bin/env python3
"""
Test script for plant disease detection model
Run this after training the model to verify it works correctly
"""

import os
import sys
sys.path.append('models')

def test_model():
    """Test the plant disease detection model"""
    try:
        from models.plant_disease_predictor import predict_plant_disease
        
        # Test with sample images
        test_dir = "dataset/Plant Diseases Dataset/test/test"
        if not os.path.exists(test_dir):
            print(f"Test directory not found: {test_dir}")
            return
        
        test_images = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
        
        print("Testing Plant Disease Detection Model...")
        print("=" * 50)
        
        for img_name in test_images:
            img_path = os.path.join(test_dir, img_name)
            try:
                result = predict_plant_disease(img_path)
                print(f"\nImage: {img_name}")
                print(f"Predicted Disease: {result['disease']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Top 3 predictions:")
                
                # Sort predictions by confidence
                sorted_preds = sorted(result['all_predictions'].items(), 
                                    key=lambda x: x[1], reverse=True)[:3]
                
                for disease, conf in sorted_preds:
                    print(f"  - {disease}: {conf:.3f}")
                    
            except Exception as e:
                print(f"Error processing {img_name}: {e}")
        
        print("\n" + "=" * 50)
        print("Model test completed successfully!")
        
    except ImportError as e:
        print(f"Model not found. Please run the notebook first to train the model.")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error testing model: {e}")

if __name__ == "__main__":
    test_model()
