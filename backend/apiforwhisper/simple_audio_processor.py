import os
import whisper
import typing
from pathlib import Path

class SimpleAudioProcessor:
    def __init__(self, hf_token: typing.Optional[str] = None):
        """
        Simple audio processor for short inputs.
        Loads the Whisper model once.
        
        Args:
            hf_token: HuggingFace token for diarization (if needed in future)
        """
        print("Loading Whisper small model...")
        self.whisper_model = whisper.load_model("small")
        self.hf_token = hf_token
        if hf_token:
            print("HuggingFace token configured for future diarization features")

    def transcribe_audio(self, audio_path: str, language: typing.Optional[str] = None) -> str:
        """
        Transcribe audio using Whisper (supports many formats directly)
        """
        print(f"Transcribing audio: {audio_path}")
        
        # Check if file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Check file size
        file_size = os.path.getsize(audio_path)
        print(f"File size: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("Audio file is empty")
        
        try:
            result = self.whisper_model.transcribe(
                audio_path,
                language=language,
                word_timestamps=False,
                verbose=False  # Disable verbose to avoid Unicode output issues
            )
            print("Transcription completed")
            # Ensure the text is properly encoded
            text = result['text'].encode('utf-8', errors='ignore').decode('utf-8')
            return text
        except Exception as e:
            print(f"Error during transcription: {e}")
            print(f"Error type: {type(e).__name__}")
            raise
