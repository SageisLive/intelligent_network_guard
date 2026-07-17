from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import time
import network_scanner as scanner
import system_monitor as monitor

app = FastAPI(title="Phishing Threat Detection API", version="1.0.0")

# Define the Security Access Header
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_token(api_key: str = Security(api_key_header)):
    if api_key != "Bearer valid_token_2026":
        raise HTTPException(status_code=401, detail="Unauthorized client: Missing or invalid access token")
    return api_key

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ThreatTarget(BaseModel):
    target_url: str
    request_id: str
    priority_level: int

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

# Apply the security verification to the core scanning endpoint
@app.post("/api/v1/scan")
async def execute_threat_scan(target: ThreatTarget, token: str = Depends(verify_token)):
    start_time = time.time()
    try:
        features = scanner.extract_network_features(target.target_url)
        prediction, confidence = scanner.predict_phishing_threat(features)
        
        return {
            "request_id": target.request_id,
            "status": "processed",
            "verdict": "phishing" if prediction == 1 else "legitimate",
            "confidence_score": round(float(confidence), 4),
            "latency_seconds": round(time.time() - start_time, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))