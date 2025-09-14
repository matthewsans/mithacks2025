# Tandem Search Interface with Whisper Speech-to-Text

A full-stack application that combines speech-to-text transcription using OpenAI Whisper with a ChatGPT-like search interface. Users can either type queries or use voice input to search and get HTML-formatted responses.

<img width="1232" height="682" alt="Screenshot 2025-09-14 112321" src="https://github.com/user-attachments/assets/1e464461-899a-4e64-ab81-6edb11f34a82" />

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **FFmpeg** (for audio processing)

### 1. Install FFmpeg (Required)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 2. Backend Setup (Whisper API)

```bash
# Navigate to backend directory
cd backend/apiforwhisper

# Install Python dependencies
pip install -r requirements.txt

# Create config.json with your HuggingFace token
echo '{
    "hf_token": "your_huggingface_token_here"
}' > config.json

# Start the backend server
python3 main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup (Web Interface)

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install Node.js dependencies
npm install

# Start the frontend server
npm start
```

The frontend will start on `http://localhost:3000`

### 4. Access the Application

Open your browser and go to: **http://localhost:3000**

## 🎯 Features

- **🎤 Voice Input**: Click the microphone button to record audio
- **📝 Text Input**: Type queries directly in the search box
- **�� Speech-to-Text**: Powered by OpenAI Whisper for accurate transcription
- **🔍 Search Interface**: ChatGPT-like interface for querying
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Whisper       │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Local)       │
│                 │    │                 │    │                 │
│ • Web Interface │    │ • FastAPI       │    │ • Audio         │
│ • Audio Record  │    │ • CORS Enabled  │    │   Processing    │
│ • Search UI     │    │ • File Upload   │    │ • Transcription │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📡 API Documentation

### Backend API (Whisper Service)

**Base URL**: `http://localhost:8000`

#### `POST /transcribe`
Transcribe audio files using OpenAI Whisper.

**Request:**
```bash
curl -X POST -F "file=@audio.wav" http://localhost:8000/transcribe
```

**Response:**
```json
{
  "text": "This is the transcribed text",
  "filename": "audio.wav",
  "success": true
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "whisper-api"
}
```

### Frontend API

**Base URL**: `http://localhost:3000`

#### `POST /api/whisper`
Process audio for speech-to-text (proxied to backend).

**Request:**
```bash
curl -X POST -F "audio=@recording.wav" http://localhost:3000/api/whisper
```

**Response:**
```json
{
  "text": "Transcribed text",
  "success": true
}
```

#### `POST /api/search`
Search with text queries (requires Tandem API configuration).

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"your search query"}' \
  http://localhost:3000/api/search
```

## ⚙️ Configuration

### Backend Configuration

**File**: `backend/apiforwhisper/config.json`
```json
{
    "hf_token": "your_huggingface_token_here"
}
```

### Frontend Configuration

**File**: `frontend/.env`
```env
# Tandem API Configuration (Optional)
# TANDEM_API_URL=https://your-tandem-api-url.com/api
# TANDEM_API_KEY=your_api_key_here

# Local Whisper API Configuration
LOCAL_WHISPER_URL=http://localhost:8000/transcribe

# Timeouts
TANDEM_API_TIMEOUT=10000
LOCAL_WHISPER_TIMEOUT=30000

# Port
PORT=3000
```

## 🛠️ Development

### Backend Development
```bash
cd backend/apiforwhisper
python3 main.py  # Starts with auto-reload
```

### Frontend Development
```bash
cd frontend
npm run dev  # Starts with nodemon for auto-reload
```

### Testing the APIs

**Test Whisper Transcription:**
```bash
# Test with empty file (should return error)
curl -X POST -F "file=@/dev/null" http://localhost:8000/transcribe

# Test with actual audio file
curl -X POST -F "file=@your_audio.wav" http://localhost:8000/transcribe
```

**Test Frontend Integration:**
```bash
# Test frontend health
curl http://localhost:3000

# Test whisper proxy
curl -X POST -F "audio=@your_audio.wav" http://localhost:3000/api/whisper
```

## 🐛 Troubleshooting

### Common Issues

**1. "ffmpeg not found" Error**
```bash
# Install ffmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu
```

**2. "Address already in use" Error**
```bash
# Kill processes using ports 8000 and 3000
lsof -ti:8000,3000 | xargs kill -9
```

**3. "Tandem API not configured" Error**
- This is expected if you haven't set up Tandem API
- The Whisper transcription will still work
- To fix: Configure `TANDEM_API_URL` and `TANDEM_API_KEY` in `.env`

**4. CORS Errors**
- The backend has CORS enabled for all origins
- If you still get CORS errors, check that the backend is running on port 8000

### Logs and Debugging

**Backend Logs:**
- Check the terminal where you ran `python3 main.py`
- Look for "Loading Whisper small model..." and "Application startup complete"

**Frontend Logs:**
- Check the terminal where you ran `npm start`
- Look for "Server running on http://localhost:3000"

## 📁 Project Structure

```
mithacks2025/
├── backend/
│   └── apiforwhisper/
│       ├── main.py              # FastAPI server
│       ├── simple_audio_processor.py
│       ├── whisper_handler.py
│       ├── config.json          # HuggingFace token
│       └── requirements.txt
├── frontend/
│   ├── index.html              # Web interface
│   ├── server.js               # Express server
│   ├── package.json
│   └── .env                    # Environment variables
└── README.md
```

## 🔧 Dependencies

### Backend Dependencies
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `python-multipart==0.0.6` - File upload support
- `openai-whisper==20231117` - Speech-to-text
- `torch` - ML framework
- `torchaudio` - Audio processing
- `ffmpeg-python` - Audio format support

### Frontend Dependencies
- `express` - Web server
- `cors` - Cross-origin requests
- `multer` - File upload handling
- `dotenv` - Environment variables

## 📝 Usage Examples

### Using the Web Interface

1. **Voice Input:**
   - Click the microphone button
   - Allow microphone access when prompted
   - Speak your query
   - The text will be transcribed and auto-submitted

2. **Text Input:**
   - Type your query in the search box
   - Press Enter or click Search

### Using the API Directly

**Transcribe Audio:**
```bash
curl -X POST -F "file=@recording.wav" http://localhost:8000/transcribe
```

**Get Health Status:**
```bash
curl http://localhost:8000/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure both servers are running
4. Check the logs for error messages

For additional help, please open an issue in the repository.
