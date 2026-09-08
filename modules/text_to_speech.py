#!/usr/bin/env python3
"""
Text-to-Speech Module
تحويل النص إلى كلام
"""

import logging
import os
from typing import Dict, Optional
from pydub import AudioSegment
from pydub.generators import Sine
import subprocess

logger = logging.getLogger(__name__)

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    logger.warning("Google Cloud Text-to-Speech not installed")

class TextToSpeechGenerator:
    """Convert text to speech for video narration"""
    
    def __init__(self, config):
        self.language = config.get('CONTENT_LANGUAGE', 'ar')
        self.output_dir = 'generated_audio'
        self._create_output_directory()
        logger.info(f"TextToSpeechGenerator initialized for language: {self.language}")
    
    def _create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_narration(self, script: str, voice: str = 'male', 
                          speed: float = 1.0, output_file: str = None) -> Dict:
        """
        Generate narration audio from script
        
        Args:
            script: Video script text
            voice: Voice type (male, female, child)
            speed: Speech speed (0.5 - 2.0)
            output_file: Path to save audio
        
        Returns:
            Dictionary with audio file path
        """
        try:
            if output_file is None:
                output_file = f"{self.output_dir}/narration_{hash(script)}.mp3"
            
            if GOOGLE_TTS_AVAILABLE:
                return self._generate_with_google(script, voice, speed, output_file)
            else:
                logger.warning("Using fallback TTS method")
                return self._generate_with_espeak(script, output_file)
        
        except Exception as e:
            logger.error(f"Error generating narration: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_with_google(self, script: str, voice: str, 
                             speed: float, output_file: str) -> Dict:
        """Generate speech using Google Cloud TTS"""
        try:
            client = texttospeech.TextToSpeechClient()
            
            # Map voice type to Google voices
            voice_map = {
                'male': 'ar-XA-Standard-B',
                'female': 'ar-XA-Standard-A',
                'child': 'ar-XA-Standard-C'
            }
            
            synthesis_input = texttospeech.SynthesisInput(text=script)
            
            voice_params = texttospeech.VoiceSelectionParams(
                language_code="ar-SA",
                name=voice_map.get(voice, voice_map['male'])
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speed
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )
            
            with open(output_file, 'wb') as out:
                out.write(response.audio_content)
            
            logger.info(f"Narration generated: {output_file}")
            return {
                "status": "success",
                "audio_file": output_file,
                "duration": self._get_audio_duration(output_file)
            }
        
        except Exception as e:
            logger.error(f"Google TTS error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_with_espeak(self, script: str, output_file: str) -> Dict:
        """Generate speech using espeak fallback"""
        try:
            cmd = [
                'espeak',
                '-v', f'ar',
                '-w', output_file,
                script
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Narration generated with espeak: {output_file}")
                return {
                    "status": "success",
                    "audio_file": output_file,
                    "duration": self._get_audio_duration(output_file)
                }
            else:
                return {"status": "error", "message": result.stderr}
        
        except Exception as e:
            logger.error(f"Espeak error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def add_background_music(self, video_file: str, audio_file: str, 
                            music_file: str, output_file: str,
                            music_volume: float = 0.3) -> Dict:
        """
        Add background music to narration
        
        Args:
            video_file: Video file path
            audio_file: Narration audio file
            music_file: Background music file
            output_file: Output video file
            music_volume: Music volume level (0-1)
        
        Returns:
            Dictionary with result
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-i', music_file,
                '-filter_complex',
                f'[1:a][2:a]amerge=inputs=2[a]',
                '-map', '0:v',
                '-map', '[a]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Background music added: {output_file}")
                return {
                    "status": "success",
                    "output_file": output_file
                }
            else:
                return {"status": "error", "message": result.stderr}
        
        except Exception as e:
            logger.error(f"Error adding background music: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _get_audio_duration(self, audio_file: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio = AudioSegment.from_file(audio_file)
            return len(audio) / 1000.0  # Convert to seconds
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            return 0.0