#!/usr/bin/env python3
"""
Setup script for plant disease detection environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages for plant disease detection"""
    
    print("Setting up Plant Disease Detection Environment...")
    print("=" * 50)
    
    # Check if we're in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠️  Warning: Not in virtual environment. Consider activating .venv")
    
    # Install requirements
    requirements_file = "requirements_plant_disease.txt"
    
    if os.path.exists(requirements_file):
        print(f"\nInstalling packages from {requirements_file}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print("✓ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False
    else:
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    # Verify TensorFlow installation
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__} installed successfully")
        
        # Check GPU availability
        if tf.config.list_physical_devices('GPU'):
            print("✓ GPU support available")
        else:
            print("ℹ️  Running on CPU (GPU not available)")
            
    except ImportError:
        print("❌ TensorFlow installation failed")
        return False
    
    print("\n" + "=" * 50)
    print("Environment setup completed!")
    print("\nNext steps:")
    print("1. Open notebooks/plant_disease_detection.ipynb")
    print("2. Run all cells to train the model")
    print("3. Test with: python test_plant_disease_model.py")
    
    return True

if __name__ == "__main__":
    install_requirements()
