from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
import shutil
import json
from pathlib import Path
from backend.apiforwhisper.simple_audio_processor import SimpleAudioProcessor

# Initialize FastAPI app
app = FastAPI(title="Speech-to-Text API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config from config.json
def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config()
# Initialize the processor with HF token from config
processor = SimpleAudioProcessor(hf_token=config.get("hf_token"))

@app.post("/transcribe")
async def transcribe_file(
    file: UploadFile = File(...),
    language: str = Form(None)  # Optional: e.g. "en", "ja", etc.
):
    """
    Accepts an uploaded audio file and returns transcription
    Frontend-compatible endpoint
    """
    # Save file to a temp location
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / str(file.filename)
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            print(f"Processing file: {tmp_path}")
            result = processor.transcribe_audio(str(tmp_path), language)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    # Return format that matches frontend expectations
    return {
        "text": result,  # Changed from "transcription" to "text"
        "filename": file.filename,
        "success": True
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "whisper-api"}

# Enable server startup - UNCOMMENTED
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
