import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json
from groq import Groq
import os
from dotenv import load_dotenv
import base64
import io

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class PlantImageAnalyzer:
    def __init__(self):
        self.color_ranges = {
            'brown_spots': ([10, 50, 20], [20, 255, 200]),
            'yellow_areas': ([20, 50, 50], [30, 255, 255]),
            'white_powdery': ([0, 0, 200], [180, 30, 255]),
            'black_spots': ([0, 0, 0], [180, 255, 50]),
            'healthy_green': ([35, 50, 50], [85, 255, 255])
        }
    
    def analyze_plant_image(self, image_path: str) -> dict:
        """Comprehensive plant image analysis"""
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Basic image analysis
            basic_analysis = self._basic_image_analysis(image)
            
            # Color analysis for disease detection
            color_analysis = self._analyze_colors(image)
            
            # Texture and pattern analysis
            texture_analysis = self._analyze_texture(image)
            
            # AI-powered detailed analysis
            ai_analysis = self._ai_image_analysis(image_path)
            
            return {
                "success": True,
                "basic_analysis": basic_analysis,
                "color_analysis": color_analysis,
                "texture_analysis": texture_analysis,
                "ai_analysis": ai_analysis,
                "comprehensive_assessment": self._generate_assessment(
                    basic_analysis, color_analysis, texture_analysis, ai_analysis
                )
            }
            
        except Exception as e:
            return {"error": f"Image analysis failed: {str(e)}"}
    
    def _basic_image_analysis(self, image):
        """Basic image properties analysis"""
        height, width = image.shape[:2]
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Calculate basic statistics
        brightness = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        
        return {
            "image_dimensions": {"width": width, "height": height},
            "brightness_level": float(brightness),
            "overall_color_distribution": self._get_dominant_colors(image)
        }
    
    def _analyze_colors(self, image):
        """Analyze colors for disease indicators"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        results = {}
        
        for condition, (lower, upper) in self.color_ranges.items():
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv, lower, upper)
            percentage = (np.sum(mask > 0) / mask.size) * 100
            
            results[condition] = {
                "percentage": float(percentage),
                "severity": "high" if percentage > 15 else "medium" if percentage > 5 else "low"
            }
        
        return results
    
    def _analyze_texture(self, image):
        """Analyze texture patterns for disease detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection for spot analysis
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Contour analysis for spot counting
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contour properties
        spot_analysis = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Filter small noise
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                spot_analysis.append({
                    "area": float(area),
                    "circularity": float(circularity),
                    "shape": "circular" if circularity > 0.7 else "irregular"
                })
        
        return {
            "edge_density": float(edge_density),
            "spot_count": len(spot_analysis),
            "spot_details": spot_analysis[:10],  # Top 10 spots
            "texture_roughness": self._calculate_texture_roughness(gray)
        }
    
    def _calculate_texture_roughness(self, gray_image):
        """Calculate texture roughness using local binary patterns"""
        # Simple texture measure using standard deviation
        kernel = np.ones((5,5), np.float32) / 25
        smooth = cv2.filter2D(gray_image, -1, kernel)
        roughness = np.std(gray_image - smooth)
        return float(roughness)
    
    def _get_dominant_colors(self, image):
        """Get dominant colors in the image"""
        # Reshape image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Use k-means to find dominant colors
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        percentages = np.bincount(kmeans.labels_) / len(kmeans.labels_) * 100
        
        return [
            {"color_bgr": color.tolist(), "percentage": float(pct)}
            for color, pct in zip(colors, percentages)
        ]
    
    def _ai_image_analysis(self, image_path):
        """AI-powered detailed image analysis using Groq"""
        try:
            # Convert image to base64 for AI analysis
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
            
            prompt = """
            Analyze this plant image and provide detailed information about:
            
            1. SPOT CHARACTERISTICS:
               - Color of spots (brown, black, yellow, white, etc.)
               - Size and shape of spots (small/large, circular/irregular)
               - Texture (raised/flat, dry/wet, fuzzy/smooth)
               - Distribution pattern (scattered/clustered/edge-focused)
            
            2. LEAF CONDITION:
               - Overall leaf color and health
               - Signs of wilting, curling, or deformation
               - Leaf surface texture and appearance
               - Any unusual growths or coatings
            
            3. PLANT HEALTH INDICATORS:
               - Overall plant vigor
               - Signs of stress or disease progression
               - Affected plant parts (leaves, stems, fruits)
               - Environmental stress indicators
            
            4. DISEASE SYMPTOMS:
               - Primary symptoms visible
               - Secondary symptoms
               - Disease progression stage
               - Severity assessment
            
            Provide detailed, specific observations in JSON format.
            """
            
            response = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.2
            )
            
            return {
                "ai_observations": response.choices[0].message.content,
                "analysis_confidence": "high"
            }
            
        except Exception as e:
            return {
                "ai_observations": "AI analysis unavailable",
                "analysis_confidence": "low",
                "error": str(e)
            }
    
    def _generate_assessment(self, basic, color, texture, ai):
        """Generate comprehensive plant health assessment"""
        assessment = {
            "overall_health": "unknown",
            "disease_indicators": [],
            "severity_level": "unknown",
            "recommendations": []
        }
        
        # Analyze color indicators
        disease_indicators = []
        if color.get("brown_spots", {}).get("percentage", 0) > 10:
            disease_indicators.append("Brown spot disease likely")
        if color.get("yellow_areas", {}).get("percentage", 0) > 20:
            disease_indicators.append("Nutrient deficiency or viral infection")
        if color.get("white_powdery", {}).get("percentage", 0) > 5:
            disease_indicators.append("Powdery mildew suspected")
        if color.get("black_spots", {}).get("percentage", 0) > 5:
            disease_indicators.append("Bacterial or fungal infection")
        
        # Analyze texture indicators
        if texture.get("spot_count", 0) > 20:
            disease_indicators.append("Multiple lesions detected")
        if texture.get("texture_roughness", 0) > 30:
            disease_indicators.append("Abnormal leaf texture")
        
        # Determine severity
        total_disease_percentage = sum([
            color.get("brown_spots", {}).get("percentage", 0),
            color.get("yellow_areas", {}).get("percentage", 0),
            color.get("white_powdery", {}).get("percentage", 0),
            color.get("black_spots", {}).get("percentage", 0)
        ])
        
        if total_disease_percentage > 30:
            assessment["severity_level"] = "severe"
            assessment["overall_health"] = "poor"
        elif total_disease_percentage > 15:
            assessment["severity_level"] = "moderate"
            assessment["overall_health"] = "fair"
        elif total_disease_percentage > 5:
            assessment["severity_level"] = "mild"
            assessment["overall_health"] = "good"
        else:
            assessment["severity_level"] = "minimal"
            assessment["overall_health"] = "healthy"
        
        assessment["disease_indicators"] = disease_indicators
        
        # Generate recommendations
        recommendations = []
        if "Brown spot disease likely" in disease_indicators:
            recommendations.append("Apply copper-based fungicide")
        if "Powdery mildew suspected" in disease_indicators:
            recommendations.append("Improve air circulation and apply fungicide")
        if "Nutrient deficiency" in str(disease_indicators):
            recommendations.append("Check soil nutrients and adjust fertilization")
        if assessment["severity_level"] in ["severe", "moderate"]:
            recommendations.append("Remove severely affected leaves")
            recommendations.append("Increase monitoring frequency")
        
        assessment["recommendations"] = recommendations
        
        return assessment

# Initialize the analyzer
plant_analyzer = PlantImageAnalyzer()

def analyze_plant_image_comprehensive(image_path: str) -> dict:
    """Main function for comprehensive plant image analysis"""
    return plant_analyzer.analyze_plant_image(image_path)
