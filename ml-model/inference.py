import os
import torch
import torch.nn.functional as F
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image

class WasteClassifier:
    """
    Singleton wrapper for the Waste Classification Model to be used in production (e.g., FastAPI).
    """
    def __init__(self, weights_path="weights/best_model.pth", classes_path="weights/classes.pt"):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"[INFO] Initializing Inference Model on: {self.device}")
        
        # 1. Load Classes
        if not os.path.exists(classes_path):
            print(f"[WARNING] Classes specific file not found at {classes_path}. Using defaults.")
            self.class_names = ['biodegradable', 'recyclable', 'hazardous']
        else:
            self.class_names = torch.load(classes_path)
            
        print(f"[INFO] Loaded Classes: {self.class_names}")
        
        # 2. Rebuild Architecture 
        self.model = models.mobilenet_v2()
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Sequential(
            nn.Dropout(p=0.4),
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(512, len(self.class_names))
        )
        
        # 3. Load Weights
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Missing weights file at {weights_path}")
            
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval() # MUST set to evaluation mode
        
        # 4. Define Inference Transform (Same as test_transform from dataset.py)
        imagenet_mean = [0.485, 0.456, 0.406]
        imagenet_std = [0.229, 0.224, 0.225]
        
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),               
            transforms.CenterCrop(224),                  
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std)
        ])
        print("[INFO] Model successfully loaded and ready for inference.")

    def predict(self, image_path: str):
        """
        Runs an image through the model and returns prediction details.
        
        Returns:
            dict: { "category": str, "confidence": float, "all_probabilities": dict }
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        try:
            # Load and convert image to RGB
            img = Image.open(image_path).convert('RGB')
            
            # Apply transforms and add batch dimension (C, H, W) -> (1, C, H, W)
            input_tensor = self.transform(img).unsqueeze(0).to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                
                # Apply Softmax to get probabilities (0 to 1)
                probabilities = F.softmax(outputs, dim=1).squeeze(0)
                
                # Get the top prediction
                confidence, predicted_idx = torch.max(probabilities, 0)
                
            predicted_class = self.class_names[predicted_idx.item()]
            
            # Create a dictionary of all class probabilities
            all_probs = {
                self.class_names[i]: float(probabilities[i].item()) 
                for i in range(len(self.class_names))
            }
            
            return {
                "category": predicted_class,
                "confidence": float(confidence.item()),
                "all_probabilities": all_probs
            }
            
        except Exception as e:
            print(f"[ERROR] Inference failed on {image_path}: {str(e)}")
            raise e


# ==============================================================================
# Helper Function for quick CLI testing
# ==============================================================================
def predict_image(image_path: str, weights_path: str = "weights/best_model.pth"):
    """
    Standalone function to quickly test a single image.
    Usage: result = predict_image('test_apple.jpg')
    """
    classifier = WasteClassifier(weights_path=weights_path)
    result = classifier.predict(image_path)
    
    print("\n" + "="*40)
    print(f"PREDICTION RESULTS FOR : {os.path.basename(image_path)}")
    print("="*40)
    print(f"Predicted Category:   {result['category'].upper()}")
    print(f"Confidence Score:     {result['confidence'] * 100:.2f} %")
    print("-" * 40)
    print("All Probabilities:")
    for cat, prob in result['all_probabilities'].items():
        print(f"  {cat.ljust(15)}: {prob * 100:.2f} %")
    print("="*40 + "\n")
    
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test Waste Classifier Inference")
    parser.add_argument('image_path', type=str, help='Path to the image file to classify')
    parser.add_argument('--weights', type=str, default='weights/best_model.pth', help='Path to model weights')
    
    args = parser.parse_args()
    predict_image(args.image_path, args.weights)
