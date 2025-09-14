# Speech-to-Text API Backend

FastAPI backend for Google Cloud Speech-to-Text V1 API integration.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Cloud credentials:**
   - Create a Google Cloud project
   - Enable the Speech-to-Text API
   - Create a service account and download the JSON key file
   - Set the environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
     ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the server:**
   ```bash
   python whisper_handler.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn whisper_handler:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### `POST /transcribe`
Transcribe audio files using Google Cloud Speech-to-Text V1 API.

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
  "billing_info": "Using Speech-to-Text V1 API with data logging (free for first 60 minutes/month)"
}
```

### `POST /transcribe-long`
For audio files > 10MB or longer duration with speaker diarization support.

### `GET /languages`
Get supported language codes.

### `GET /health`
Health check endpoint.

## Pricing (Google Cloud Speech-to-Text V1)

- **With data logging:** Free for first 60 minutes/month, then $0.016/minute
- **Without data logging:** Free for first 60 minutes/month, then $0.024/minute
- **Medical model:** Free for first 60 minutes/month, then $0.078/minute

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
