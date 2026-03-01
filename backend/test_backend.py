import os
import requests
from PIL import Image
import io

BASE_URL = "http://localhost:8000/api/v1"

def create_test_image(filename="test_image.jpg"):
    """Creates a temporary dummy image for testing."""
    img = Image.new('RGB', (224, 224), color = 'green')
    img.save(filename)
    return filename

def test_carbon_endpoint():
    print("\n--- Testing POST /carbon/calculate ---")
    payload = {
        "category": "recyclable",
        "weight_grams": 200.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/carbon/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["category"] == "recyclable"
        assert data["co2_saved_grams"] > 0
        print("✅ Carbon calculation endpoint is working.")
        print(f"Data: {data}")
    except Exception as e:
        print(f"❌ Carbon calculation endpoint failed: {e}")

def test_predict_endpoint():
    print("\n--- Testing POST /predict ---")
    img_filename = create_test_image()
    
    try:
        with open(img_filename, "rb") as img_file:
            files = {"image": (img_filename, img_file, "image/jpeg")}
            data = {"weight_grams": 150.0}
            
            response = requests.post(f"{BASE_URL}/predict/", files=files, data=data)
            assert response.status_code == 200
            res_data = response.json()
            
            assert res_data["success"] is True
            assert "category" in res_data
            assert "confidence" in res_data
            assert res_data["co2_saved_grams"] >= 0
            
            print("✅ Prediction endpoint is working.")
            print(f"Detected Category: {res_data['category']}")
            print(f"Confidence: {res_data['confidence']}")
    except Exception as e:
        print(f"❌ Prediction endpoint failed: {e}")
    finally:
        if os.path.exists(img_filename):
            os.remove(img_filename)

def test_analytics_endpoint():
    print("\n--- Testing GET /analytics/dashboard ---")
    try:
        response = requests.get(f"{BASE_URL}/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "total_scans" in data["data"]
        print("✅ Analytics endpoint is working.")
        print(f"Total Scans Logged: {data['data']['total_scans']}")
    except Exception as e:
        print(f"❌ Analytics endpoint failed: {e}")

if __name__ == "__main__":
    print("====================================")
    print("STARTING BACKEND INTEGRATION TESTS")
    print("Ensure backend is running on port 8000")
    print("====================================")
    
    try:
        # Check if server is reachable
        requests.get("http://localhost:8000/")
        test_carbon_endpoint()
        test_predict_endpoint()
        test_analytics_endpoint()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to backend. Please run 'python main.py' in the backend directory first.")
