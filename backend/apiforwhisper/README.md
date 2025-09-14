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

## Main Endpoint

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

**Parameters:**
- `file`: Audio file (WAV, MP3, MP4, etc.)
- `language`: Language code (optional, e.g. "en", "ja", "es")

**Response:**
```json
{
  "transcription": "Hello world, this is the transcribed text",
  "filename": "audio_file.wav"
}
```

## Supported Audio Formats

- WAV
- MP3
- MP4
- FLAC
- OGG
- WebM
- And many more (handled by FFmpeg)

## Notes

- First run will download Whisper model (~150MB for "small" model)
- Processing time depends on audio length and system performance
- Uses OpenAI Whisper "small" model for good balance of speed and accuracy
