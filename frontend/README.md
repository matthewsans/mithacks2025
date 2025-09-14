# Frontend - Tandem Search Interface

A modern web interface for speech-to-text search functionality with a ChatGPT-like design.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ with npm
- Backend server running on port 8000

### Installation & Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env  # (if available)
# Or create .env manually with the configuration below

# Start the development server
npm start
```

The application will be available at: **http://localhost:3000**

## ⚙️ Configuration

Create a `.env` file in the frontend directory:

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

## 🎯 Features

- **🎤 Voice Input**: Click microphone to record and transcribe speech
- **📝 Text Input**: Type queries directly in the search box
- **🔄 Real-time Processing**: Live audio recording and transcription
- **📱 Responsive Design**: Works on desktop and mobile
- **🎨 Modern UI**: ChatGPT-inspired interface design

## 📡 API Endpoints

### `POST /api/whisper`
Process audio files for speech-to-text transcription.

**Request:**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.wav');

fetch('/api/whisper', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.text));
```

**Response:**
```json
{
  "text": "Transcribed text from audio",
  "success": true
}
```

### `POST /api/search`
Search with text queries (requires Tandem API).

**Request:**
```javascript
fetch('/api/search', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: 'your search query' })
})
.then(response => response.json())
.then(data => console.log(data.html));
```

**Response:**
```json
{
  "success": true,
  "html": "<div>Search results HTML</div>",
  "query": "your search query"
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "tandem_configured": false,
  "whisper_configured": true,
  "whisper_type": "local",
  "timestamp": "2025-01-14T02:27:00.000Z"
}
```

## 🛠️ Development

### Available Scripts

```bash
# Start development server
npm start

# Start with auto-reload (if nodemon is installed)
npm run dev

# Install nodemon for development
npm install -g nodemon
```

### File Structure

```
frontend/
├── index.html          # Main web interface
├── server.js           # Express server with API endpoints
├── package.json        # Dependencies and scripts
├── .env               # Environment configuration
└── README.md          # This file
```

## 🎨 UI Components

### Main Interface
- **Header**: Application title
- **Content Area**: Displays search results and HTML content
- **Search Form**: Text input and microphone button
- **Loading States**: Visual feedback during processing

### Microphone Functionality
- **Recording Indicator**: Visual feedback when recording
- **Audio Processing**: Automatic transcription after recording
- **Error Handling**: User-friendly error messages

## 🔧 Dependencies

- `express` - Web server framework
- `cors` - Cross-origin resource sharing
- `multer` - File upload middleware
- `dotenv` - Environment variable management

## 🐛 Troubleshooting

### Common Issues

**1. "Tandem API not configured" Error**
- This is expected if Tandem API is not set up
- Whisper transcription will still work
- Configure `TANDEM_API_URL` and `TANDEM_API_KEY` in `.env` to fix

**2. "Local Whisper API not configured" Error**
- Ensure backend is running on port 8000
- Check `LOCAL_WHISPER_URL` in `.env` file

**3. Microphone Access Denied**
- Allow microphone permissions in browser
- Use HTTPS in production for microphone access

**4. CORS Errors**
- Backend has CORS enabled
- Ensure backend is running on correct port

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
```

## 📱 Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

**Note**: Microphone access requires HTTPS in production environments.

## 🚀 Production Deployment

### Environment Variables
```env
NODE_ENV=production
PORT=3000
LOCAL_WHISPER_URL=http://your-backend-server:8000/transcribe
TANDEM_API_URL=https://your-tandem-api.com/api
TANDEM_API_KEY=your_production_api_key
```

### Build for Production
```bash
# Install production dependencies only
npm install --production

# Start with PM2 (recommended)
npm install -g pm2
pm2 start server.js --name "tandem-frontend"
```

## 📄 License

This project is part of the Tandem Search Interface and is licensed under the MIT License.
