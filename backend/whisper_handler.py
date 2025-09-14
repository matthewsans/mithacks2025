import os
import io
import tempfile
from typing import Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.cloud import speech
from google.cloud.speech import RecognitionAudio, RecognitionConfig
from dotenv import load_dotenv
import uvicorn
import aiofiles
import traceback


# Load environment variables
load_dotenv()

app = FastAPI(
    title="Speech-to-Text API",
    description="Google Cloud Speech-to-Text V1 API with FastAPI",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Cloud Speech client
def get_speech_client():
    """Initialize and return Google Cloud Speech client"""
    try:
        # Set up credentials if provided
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        client = speech.SpeechClient()
        return client

    except Exception as e:
        traceback.print_exc()  # Logs full traceback to console
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e) or 'Unknown error'}"
        )


def get_supported_languages():
    """Return supported language codes for Google Cloud Speech-to-Text"""
    return {
        "en-US": "English (United States)",
        "en-GB": "English (United Kingdom)",
        "es-ES": "Spanish (Spain)",
        "es-US": "Spanish (United States)",
        "fr-FR": "French (France)",
        "de-DE": "German (Germany)",
        "it-IT": "Italian (Italy)",
        "pt-BR": "Portuguese (Brazil)",
        "ja-JP": "Japanese (Japan)",
        "ko-KR": "Korean (South Korea)",
        "zh-CN": "Chinese (Mandarin, Simplified)",
        "zh-TW": "Chinese (Mandarin, Traditional)",
        "ar-SA": "Arabic (Saudi Arabia)",
        "hi-IN": "Hindi (India)",
        "ru-RU": "Russian (Russia)",
        "nl-NL": "Dutch (Netherlands)",
        "sv-SE": "Swedish (Sweden)",
        "da-DK": "Danish (Denmark)",
        "no-NO": "Norwegian (Norway)",
        "fi-FI": "Finnish (Finland)"
    }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Speech-to-Text API is running", "status": "healthy"}

@app.get("/languages")
async def get_languages():
    """Get supported languages"""
    return {"languages": get_supported_languages()}

@app.post("/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language_code: str = Form(default="en-US"),
    enable_automatic_punctuation: bool = Form(default=True),
    enable_word_time_offsets: bool = Form(default=False),
    model: str = Form(default="latest_short")
):
    """
    Transcribe audio file using Google Cloud Speech-to-Text V1 API
    
    - **audio_file**: Audio file to transcribe (WAV, FLAC, MP3, etc.)
    - **language_code**: Language code (e.g., en-US, es-ES)
    - **enable_automatic_punctuation**: Add punctuation to transcript
    - **enable_word_time_offsets**: Include word-level timestamps
    - **model**: Recognition model (default, latest_long, latest_short, command_and_search, phone_call, video, medical_dictation)
    """
    
    # Validate file type
    allowed_types = [
        "audio/wav", "audio/x-wav", "audio/flac", "audio/x-flac",
        "audio/mpeg", "audio/mp3", "audio/ogg", "audio/webm",
        "audio/amr", "audio/3gpp"
    ]
    
    if audio_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {audio_file.content_type}. Supported types: {allowed_types}"
        )
    
    # Validate language code
    supported_languages = get_supported_languages()
    if language_code not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language code: {language_code}. Supported languages: {list(supported_languages.keys())}"
        )
    
    try:
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Initialize Speech client
        client = get_speech_client()
        
        # Configure recognition settings
        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            enable_word_time_offsets=enable_word_time_offsets,
            model=model,
            use_enhanced=True,
            enable_word_confidence=True
        )

        
        # Create recognition audio object
        audio = RecognitionAudio(content=audio_content)
        
        # Perform speech recognition
        response = client.recognize(config=config, audio=audio)
        
        # Process results
        transcripts = []
        for result in response.results:
            alternative = result.alternatives[0]
            
            transcript_data = {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence
            }
            
            # Add word-level timestamps if requested
            if enable_word_time_offsets and hasattr(alternative, 'words'):
                words = []
                for word_info in alternative.words:
                    words.append({
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                        "confidence": getattr(word_info, 'confidence', None)
                    })
                transcript_data["words"] = words
            
            transcripts.append(transcript_data)
        
        # Calculate estimated cost (for reference)
        audio_duration_minutes = len(audio_content) / (16000 * 2 * 60)  # Rough estimate
        estimated_cost = 0.0 if audio_duration_minutes <= 60 else (audio_duration_minutes - 60) * 0.016
        
        return JSONResponse(content={
            "success": True,
            "transcripts": transcripts,
            "language_code": language_code,
            "model": model,
            "file_info": {
                "filename": audio_file.filename,
                "content_type": audio_file.content_type,
                "size_bytes": len(audio_content)
            },
            "estimated_duration_minutes": round(audio_duration_minutes, 2),
            "estimated_cost_usd": round(estimated_cost, 4),
            "billing_info": "Using Speech-to-Text V1 API with data logging (free for first 60 minutes/month)"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/transcribe-long")
async def transcribe_long_audio(
    audio_file: UploadFile = File(...),
    language_code: str = Form(default="en-US"),
    enable_automatic_punctuation: bool = Form(default=True),
    enable_speaker_diarization: bool = Form(default=False),
    diarization_speaker_count: int = Form(default=2)
):
    """
    Transcribe long audio files using asynchronous recognition
    For files longer than 1 minute or larger than 10MB
    """
    
    try:
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Check if file is large enough to warrant long-running recognition
        if len(audio_content) < 10 * 1024 * 1024:  # Less than 10MB
            raise HTTPException(
                status_code=400,
                detail="Use /transcribe endpoint for smaller files. This endpoint is for files > 10MB"
            )
        
        # Initialize Speech client
        client = get_speech_client()
        
        # Configure recognition settings for long audio
        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=0,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            model="latest_long",  # Optimized for long audio
            use_enhanced=True
        )
        
        # Add speaker diarization if requested
        if enable_speaker_diarization:
            diarization_config = speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
                min_speaker_count=1,
                max_speaker_count=diarization_speaker_count,
            )
            config.diarization_config = diarization_config
        
        # Create recognition audio object
        audio = RecognitionAudio(content=audio_content)
        
        # Start long-running recognition
        operation = client.long_running_recognize(config=config, audio=audio)
        
        # For demo purposes, we'll wait for completion
        # In production, you might want to return operation name and check status separately
        response = operation.result(timeout=300)  # 5 minute timeout
        
        # Process results
        transcripts = []
        for result in response.results:
            alternative = result.alternatives[0]
            
            transcript_data = {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence
            }
            
            # Add speaker information if diarization was enabled
            if enable_speaker_diarization and hasattr(alternative, 'words'):
                words = []
                for word_info in alternative.words:
                    words.append({
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                        "speaker_tag": getattr(word_info, 'speaker_tag', 0)
                    })
                transcript_data["words"] = words
            
            transcripts.append(transcript_data)
        
        return JSONResponse(content={
            "success": True,
            "transcripts": transcripts,
            "language_code": language_code,
            "model": "latest_long",
            "speaker_diarization_enabled": enable_speaker_diarization,
            "file_info": {
                "filename": audio_file.filename,
                "content_type": audio_file.content_type,
                "size_bytes": len(audio_content)
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Long audio transcription failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test Google Cloud Speech client initialization
        client = get_speech_client()
        
        return {
            "status": "healthy",
            "speech_client": "connected",
            "supported_languages": len(get_supported_languages()),
            "environment": os.getenv("ENVIRONMENT", "production")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "speech_client": "failed"
        }

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "whisper_handler:app",
        host=host,
        port=port,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )