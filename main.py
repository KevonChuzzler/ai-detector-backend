import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AI Content Detector API", version="1.0.0")

class ScanRequest(BaseModel):
    client_id: str = Field(..., description="App client identifier")
    content_type: str = Field(..., description="'text' or 'image_base64'")
    text_payload: str | None = Field(None, description="Extracted text from screen")
    image_data: str | None = Field(None, description="Base64 encoded image string")

class ScanResponse(BaseModel):
    status: str
    ai_probability: float
    human_probability: float
    verdict: str
    processing_time_ms: int

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/v1/scan", response_model=ScanResponse)
async def scan_content(request: ScanRequest):
    start_time = time.time()

    if request.content_type == "text" and not request.text_payload:
        raise HTTPException(status_code=400, detail="Text payload is missing.")
    if request.content_type == "image_base64" and not request.image_data:
        raise HTTPException(status_code=400, detail="Image payload is missing.")

    # Simulated AI classification engine
    # In production, pass request.text_payload to ONNX Runtime model here
    mock_ai_score = 88.5
    mock_human_score = round(100.0 - mock_ai_score, 2)
    verdict = "likely_ai" if mock_ai_score > 70.0 else "likely_human"

    elapsed_ms = int((time.time() - start_time) * 1000)

    return {
        "status": "success",
        "ai_probability": mock_ai_score,
        "human_probability": mock_human_score,
        "verdict": verdict,
        "processing_time_ms": elapsed_ms
    }