
#  Eco Waste Analyzer

### AI-Powered Waste Classification + Environmental Impact Calculator

Eco Waste Analyzer is an end-to-end AI application that identifies waste types (Biodegradable, Recyclable, Hazardous) from an image and calculates the CO₂ emissions saved by proper disposal.
It includes:

* **React Frontend (Vite)**
* **FastAPI Backend**
*  **Deep Learning Model (MobileNetV2)**
*  **Custom-trained Waste Classifier**
*  **Fully deployable on Render + Vercel**

---

##  Features

###  **AI Waste Classification**

Upload an image of any waste item, and the model predicts:

* **Biodegradable**
* **Recyclable**
* **Hazardous**

The model is trained on a custom dataset of ~23,000 images using **MobileNetV2** for high accuracy and fast inference.

---

### **Environmental Impact Calculation**

The app computes:

* CO₂ savings
* Eco-impact score
* Facts about proper disposal

Super helpful for sustainability-focused projects.

---

###  **Modern Frontend (React + Vite)**

Beautiful UI with:

* Glassmorphism design
* Animations (Framer Motion)
* Drag-and-drop upload
* Real-time result card

---

###  **FastAPI Backend**

Provides clean API endpoints:

| Endpoint   | Method | Description                               |
| ---------- | ------ | ----------------------------------------- |
| `/`        | GET    | API status                                |
| `/predict` | POST   | Upload image → returns class + confidence |
| `/docs`    | GET    | Swagger API UI                            |

---

###  **Model**

* Architecture: **MobileNetV2**
* Training: 12 epochs, weighted sampling
* Accuracy: **~91%**
* Files used:

  * `weights/best_model.pth`
  * `weights/classes.pt`

---

##  Project Structure

```
eco-waste-analyzer/
│── backend/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── weights/
│   │   ├── best_model.pth
│   │   └── classes.pt
│   ├── main.py
│   ├── requirements.txt
│
│── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│
│── ml-model/
│   ├── dataset/
│   ├── train.py
│   ├── evaluate.py
│   └── inference.py
│
│── render.yaml
│── package-lock.json
```

---

## 🛠️ Setup Instructions

### ** Backend (FastAPI)**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### **2️ Frontend (React + Vite)**

```bash
cd frontend
npm install
npm run dev
```

Make sure the frontend `.env` contains:

```
VITE_API_URL=http://localhost:8000
```

---

##  Deployment

### **Render (Backend)**

* Connect GitHub repo
* Select `/backend`
* Add Build Command:

  ```
  pip install -r requirements.txt
  ```
* Start Command:

  ```
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

### **Vercel (Frontend)**

* Import project
* Set ENV variable:

  ```
  VITE_API_URL = https://your-backend.onrender.com
  ```
* Deploy 

---

##  Screenshots

*(Add your UI screenshots here if you want – optional)*

---

## Tech Stack

* **Python** (FastAPI, PyTorch, Torchvision)
* **JavaScript** (React, Vite)
* **Deep Learning** (MobileNetV2)
* **Cloud** (Render, Vercel)
* **Tools**: Postman, Swagger, GitHub, VS Code

---




