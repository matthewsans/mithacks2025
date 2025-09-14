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
<<<<<<< HEAD
=======

## Prerequisites
- Python 3.8+
- FFmpeg installed on system
>>>>>>> 6f9c974 (feat: add frontend setup with Node.js server and update backend configs)

## Main Endpoint

<<<<<<< HEAD
**POST `/transcribe`**
Upload an audio file to get transcription.

**Usage:**
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@your_audio_file.wav" \
  -F "language=en"
```

Or use the interactive docs at `http://localhost:8000/docs` to test uploads.

## Prerequisites
- Python 3.8+
- FFmpeg installed on system

## API Response
=======
### `POST /transcribe`
Transcribe audio files using OpenAI Whisper.
>>>>>>> 6f9c974 (feat: add frontend setup with Node.js server and update backend configs)

**Parameters:**
- `file`: Audio file (WAV, MP3, MP4, etc.)
- `language`: Language code (optional, e.g. "en", "ja", "es")

**Response:**
```json
{
<<<<<<< HEAD
  "transcription": "Hello world, this is the transcribed text",
  "filename": "audio_file.wav"
}
```

=======
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

>>>>>>> 6f9c974 (feat: add frontend setup with Node.js server and update backend configs)
## Supported Audio Formats

- WAV
- MP3
- MP4
- FLAC
- OGG
- WebM
- And many more (handled by FFmpeg)

## Notes

<<<<<<< HEAD
- First run will download Whisper model (~150MB for "small" model)
- Processing time depends on audio length and system performance
- Uses OpenAI Whisper "small" model for good balance of speed and accuracy
=======
A simple HTML client is provided in `/frontend/index.html` for testing the API.
>>>>>>> 6f9c974 (feat: add frontend setup with Node.js server and update backend configs)
