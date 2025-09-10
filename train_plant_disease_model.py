#!/usr/bin/env python3
"""
Direct training script for plant disease detection model
Run this instead of the notebook for automated training
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib
from sklearn.metrics import classification_report
import time

def train_plant_disease_model():
    print("🌱 Starting Plant Disease Detection Model Training...")
    print("=" * 60)
    
    # Dataset paths
    base_path = 'dataset/Plant Diseases Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)'
    train_path = os.path.join(base_path, 'train')
    valid_path = os.path.join(base_path, 'valid')
    
    # Check if dataset exists
    if not os.path.exists(train_path):
        print(f"❌ Training data not found at: {train_path}")
        return False
    
    # Model parameters
    IMG_SIZE = 224
    BATCH_SIZE = 32
    EPOCHS = 15  # Reduced for faster training
    
    print(f"📊 Configuration:")
    print(f"   - Image Size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"   - Batch Size: {BATCH_SIZE}")
    print(f"   - Epochs: {EPOCHS}")
    
    # Data preprocessing
    print("\n📁 Loading and preprocessing data...")
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    valid_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load data
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    valid_generator = valid_datagen.flow_from_directory(
        valid_path,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    NUM_CLASSES = train_generator.num_classes
    class_names = list(train_generator.class_indices.keys())
    
    print(f"✅ Data loaded successfully:")
    print(f"   - Training samples: {train_generator.samples}")
    print(f"   - Validation samples: {valid_generator.samples}")
    print(f"   - Number of classes: {NUM_CLASSES}")
    
    # Create model
    print(f"\n🤖 Building model with MobileNetV2...")
    
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"✅ Model created with {model.count_params():,} parameters")
    
    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-7
        )
    ]
    
    # Train model
    print(f"\n🚀 Starting training...")
    start_time = time.time()
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=valid_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    training_time = time.time() - start_time
    print(f"\n⏱️  Training completed in {training_time/60:.1f} minutes")
    
    # Evaluate model
    print(f"\n📊 Evaluating model...")
    test_loss, test_accuracy = model.evaluate(valid_generator, verbose=0)
    print(f"✅ Final Validation Accuracy: {test_accuracy:.4f}")
    print(f"✅ Final Validation Loss: {test_loss:.4f}")
    
    # Save model and class names
    model_path = 'models/plant_disease_model.h5'
    class_names_path = 'models/plant_disease_classes.pkl'
    
    os.makedirs('models', exist_ok=True)
    
    model.save(model_path)
    joblib.dump(class_names, class_names_path)
    
    print(f"\n💾 Model saved:")
    print(f"   - Model: {model_path}")
    print(f"   - Classes: {class_names_path}")
    print(f"   - Model size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
    
    # Create prediction utility
    prediction_code = f'''import tensorflow as tf
import numpy as np
import joblib
from tensorflow.keras.preprocessing import image

def load_plant_disease_model():
    """Load the trained plant disease detection model"""
    model = tf.keras.models.load_model('models/plant_disease_model.h5')
    class_names = joblib.load('models/plant_disease_classes.pkl')
    return model, class_names

def predict_plant_disease(image_path):
    """Predict plant disease from image path"""
    model, class_names = load_plant_disease_model()
    
    # Load and preprocess image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    
    predicted_class = class_names[predicted_class_idx]
    
    return {{
        "disease": predicted_class,
        "confidence": float(confidence),
        "all_predictions": {{class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}}
    }}
'''
    
    with open('models/plant_disease_predictor.py', 'w') as f:
        f.write(prediction_code)
    
    print(f"   - Predictor: models/plant_disease_predictor.py")
    
    # Test with sample images
    print(f"\n🧪 Testing model with sample images...")
    test_images_path = 'dataset/Plant Diseases Dataset/test/test'
    
    if os.path.exists(test_images_path):
        test_images = [f for f in os.listdir(test_images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
        
        for img_name in test_images:
            img_path = os.path.join(test_images_path, img_name)
            
            # Load and preprocess image
            img = tf.keras.preprocessing.image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0
            
            # Predict
            predictions = model.predict(img_array, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_idx]
            predicted_class = class_names[predicted_class_idx]
            
            print(f"   {img_name}: {predicted_class} ({confidence:.3f})")
    
    print(f"\n🎉 Training completed successfully!")
    print(f"=" * 60)
    
    return True

if __name__ == "__main__":
    success = train_plant_disease_model()
    if success:
        print("✅ You can now test the model with: python test_plant_disease_model.py")
    else:
        print("❌ Training failed. Please check the dataset path and try again.")
