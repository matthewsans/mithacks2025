const express = require('express');
const cors = require('cors');
const path = require('path');
const multer = require('multer');
require('dotenv').config(); // Load environment variables

const app = express();
const PORT = process.env.PORT || 3000;

// Configure multer for file uploads
const upload = multer({ 
    storage: multer.memoryStorage(),
    limits: {
        fileSize: 25 * 1024 * 1024 // 25MB limit for audio files
    }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Tandem API integration
async function callTandemAPI(query) {
    try {
        // Check if Tandem API is configured
        if (!process.env.TANDEM_API_URL || !process.env.TANDEM_API_KEY) {
            throw new Error('Tandem API not configured. Please set TANDEM_API_URL and TANDEM_API_KEY in your .env file.');
        }
        
        // Make actual API call to Tandem
        const response = await fetch(process.env.TANDEM_API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${process.env.TANDEM_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: query,
                // Add other required parameters based on Tandem API documentation
            }),
            timeout: process.env.TANDEM_API_TIMEOUT || 10000
        });
        
        if (!response.ok) {
            throw new Error(`Tandem API error: ${response.status} - ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Adjust this based on your Tandem API response structure
        // Common response formats:
        // - data.html
        // - data.content
        // - data.result.html
        // - data.response
        return data.html || data.content || data.result?.html || data.response || JSON.stringify(data);
        
    } catch (error) {
        console.error('Tandem API Error:', error);
        throw error;
    }
}

// Local Whisper API integration
async function callLocalWhisperAPI(audioBuffer) {
    try {
        // Check if local Whisper API is configured
        if (!process.env.LOCAL_WHISPER_URL) {
            throw new Error('Local Whisper API not configured. Please set LOCAL_WHISPER_URL in your .env file.');
        }
        
        // Create FormData for local Whisper API
        const formData = new FormData();
        const audioBlob = new Blob([audioBuffer], { type: 'audio/wav' });
        formData.append('file', audioBlob, 'recording.wav');
        
        // Make API call to local Whisper service
        const response = await fetch(process.env.LOCAL_WHISPER_URL, {
            method: 'POST',
            body: formData,
            timeout: process.env.LOCAL_WHISPER_TIMEOUT || 30000 // Longer timeout for local processing
        });
        
        if (!response.ok) {
            const errorText = await response.text().catch(() => 'Unknown error');
            throw new Error(`Local Whisper API error: ${response.status} - ${errorText}`);
        }
        
        const data = await response.json();
        
        // Adjust this based on your local Whisper API response structure
        // Common response formats:
        // - data.text
        // - data.transcription
        // - data.result
        // - data.response
        return data.text || data.transcription || data.result || data.response || '';
        
    } catch (error) {
        console.error('Local Whisper API Error:', error);
        throw error;
    }
}

// API endpoint for search
app.post('/api/search', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }
        
        console.log(`Search query received: ${query}`);
        
        // Call Tandem API
        const htmlContent = await callTandemAPI(query);
        
        res.json({
            success: true,
            html: htmlContent,
            query: query
        });
        
    } catch (error) {
        console.error('Error processing search:', error);
        res.status(500).json({ 
            error: 'API Error',
            message: error.message 
        });
    }
});

// API endpoint for local Whisper speech-to-text
app.post('/api/whisper', upload.single('audio'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No audio file provided' });
        }
        
        console.log(`Audio file received: ${req.file.size} bytes`);
        
        // Call local Whisper API
        const transcribedText = await callLocalWhisperAPI(req.file.buffer);
        
        res.json({
            success: true,
            text: transcribedText
        });
        
    } catch (error) {
        console.error('Error processing audio:', error);
        res.status(500).json({ 
            error: 'Audio Processing Error',
            message: error.message 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    const tandemConfigured = !!(process.env.TANDEM_API_URL && process.env.TANDEM_API_KEY);
    const whisperConfigured = !!process.env.LOCAL_WHISPER_URL;
    
    res.json({
        status: 'ok',
        tandem_configured: tandemConfigured,
        whisper_configured: whisperConfigured,
        whisper_type: 'local',
        timestamp: new Date().toISOString()
    });
});

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('Open your browser and navigate to the URL above to use the Tandem Search Interface');
    
    // Check configuration
    const tandemConfigured = !!(process.env.TANDEM_API_URL && process.env.TANDEM_API_KEY);
    const whisperConfigured = !!process.env.LOCAL_WHISPER_URL;
    
    if (!tandemConfigured) {
        console.log('⚠️  WARNING: Tandem API not configured.');
        console.log('   Create a .env file with TANDEM_API_URL and TANDEM_API_KEY');
    } else {
        console.log('✅ Tandem API configured and ready');
    }
    
    if (!whisperConfigured) {
        console.log('⚠️  WARNING: Local Whisper API not configured.');
        console.log('   Add LOCAL_WHISPER_URL to your .env file for speech-to-text functionality');
        console.log('   Example: LOCAL_WHISPER_URL=http://localhost:8000/transcribe');
    } else {
        console.log('✅ Local Whisper API configured and ready');
    }
});

module.exports = app;
