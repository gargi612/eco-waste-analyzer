from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.error_handlers import add_error_handlers
from api import predict, carbon, analytics

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for AI-Based Waste Segregation & Carbon Footprint Analyzer"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-domain.vercel.app", "*"], # Allow frontend domain explicitly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom error handlers
add_error_handlers(app)

# Include routers
app.include_router(predict.router, prefix=f"{settings.API_V1_STR}/predict", tags=["Prediction"])
app.include_router(carbon.router, prefix=f"{settings.API_V1_STR}/carbon", tags=["Carbon"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": "ok"
    }

if __name__ == "__main__":
    import uvicorn
    # When deployed locally or on Render, it listens on 0.0.0.0
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
