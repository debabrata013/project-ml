
import tensorflow as tf
import numpy as np
import joblib
from tensorflow.keras.preprocessing import image

def load_plant_disease_model():
    """Load the trained plant disease detection model"""
    model = tf.keras.models.load_model('../models/plant_disease_model.h5')
    class_names = joblib.load('../models/plant_disease_classes.pkl')
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
    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]

    predicted_class = class_names[predicted_class_idx]

    return {
        "disease": predicted_class,
        "confidence": float(confidence),
        "all_predictions": {class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}
    }
