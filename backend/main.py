# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="IntelliTraffic AI API",
    description="Backend API for Urban Traffic Monitoring and Predictive Analytics",
    version="1.0.0"
)

# Allow React frontend to communicate with the API
origins = [
    "http://localhost:5173", # Vite default port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "IntelliTraffic AI System is running."}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "IntelliTraffic Backend"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)