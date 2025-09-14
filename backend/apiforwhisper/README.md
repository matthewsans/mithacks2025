# Speech-to-Text API Backend

FastAPI backend for speech-to-text transcription using OpenAI Whisper.

## Quick Setup

**1. Install dependencies:**
```bash
pip install fastapi uvicorn python-multipart openai-whisper torch torchaudio ffmpeg-python
```

**2. Create config.json:**
```json
{
    "hf_token": "your_huggingface_token_here"
}
```

**3. Run the API:**
```bash
python -m uvicorn main:app --reload
```

**4. Access:**
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## Prerequisites
- Python 3.8+
- FFmpeg installed on system

## API Endpoints

### `POST /transcribe`
Transcribe audio files using OpenAI Whisper.

**Parameters:**
- `audio_file`: Audio file (WAV, FLAC, MP3, etc.)
- `language_code`: Language code (default: "en-US")
- `enable_automatic_punctuation`: Add punctuation (default: true)
- `enable_word_time_offsets`: Include word timestamps (default: false)
- `model`: Recognition model (default: "default")

**Response:**
```json
{
  "success": true,
  "transcripts": [
    {
      "transcript": "Hello world",
      "confidence": 0.95,
      "words": [...]
    }
  ],
  "language_code": "en-US",
  "model": "default",
  "file_info": {...},
  "estimated_duration_minutes": 1.5,
  "estimated_cost_usd": 0.0,
  "billing_info": "Using OpenAI Whisper"
}
```

### `POST /transcribe-long`
For audio files > 10MB or longer duration with speaker diarization support.

### `GET /languages`
Get supported language codes.

### `GET /health`
Health check endpoint.

## Pricing (OpenAI Whisper)

- **Free:** Open-source and self-hosted

## Supported Audio Formats

- WAV
- FLAC
- MP3
- OGG
- WebM
- AMR
- 3GPP

## Frontend Integration

A simple HTML client is provided in `/frontend/index.html` for testing the API.
