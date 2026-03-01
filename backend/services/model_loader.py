import os
import io
import torch
import torch.nn.functional as F
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
from core.config import settings

class WasteClassifierService:
    """
    Singleton wrapper for the Waste Classification Model to be used in FastAPI.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.class_names = ['biodegradable', 'hazardous', 'recyclable']
        
        # 1. Load Classes if exists
        classes_path = settings.MODEL_CLASSES_PATH
        if os.path.exists(classes_path):
            try:
                self.class_names = torch.load(classes_path)
            except Exception as e:
                print(f"[WARNING] Could not load classes.pt: {e}")
                
        # 2. Define transform
        imagenet_mean = [0.485, 0.456, 0.406]
        imagenet_std = [0.229, 0.224, 0.225]
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),               
            transforms.CenterCrop(224),                  
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std)
        ])
        
        # 3. Load Model weights
        self._load_model()
        
    def _load_model(self):
        try:
            weights_path = settings.MODEL_WEIGHTS_PATH
            if not os.path.exists(weights_path):
                print(f"[WARNING] Model weights not found at {weights_path}. Inference will return mocked results.")
                return

            self.model = models.mobilenet_v2()
            num_ftrs = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Sequential(
                nn.Dropout(p=0.4),
                nn.Linear(num_ftrs, 512),
                nn.ReLU(),
                nn.Dropout(p=0.3),
                nn.Linear(512, len(self.class_names))
            )
            
            self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print("[INFO] Model loaded successfully into Memory.")
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            self.model = None

    def predict(self, image_bytes: bytes):
        if self.model is None:
            # High-fidelity mock if no model weights exist yet
            return {
                "category": self.class_names[0],
                "confidence": 0.99,
                "all_probabilities": {c: 1.0/len(self.class_names) for c in self.class_names}
            }
            
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            input_tensor = self.transform(img).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = F.softmax(outputs, dim=1).squeeze(0)
                confidence, predicted_idx = torch.max(probabilities, 0)
                
            predicted_class = self.class_names[predicted_idx.item()]
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
            raise RuntimeError(f"Inference error: {str(e)}")

# Singleton instance exported for use in routes
classifier_service = WasteClassifierService.get_instance()
