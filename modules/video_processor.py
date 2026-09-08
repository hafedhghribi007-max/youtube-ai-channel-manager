#!/usr/bin/env python3
"""
Video Processor Module
وحدة معالجة الفيديو
"""

import logging
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import subprocess

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Process and edit videos for YouTube"""
    
    def __init__(self, config):
        self.video_quality = config.get('VIDEO_QUALITY', '720p')
        self.output_dir = 'output_videos'
        self._create_output_directory()
        logger.info(f"VideoProcessor initialized with quality: {self.video_quality}")
    
    def _create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def generate_thumbnail(self, title: str, description: str, output_file: str) -> Dict:
        """
        Generate a YouTube thumbnail image
        
        Args:
            title: Video title
            description: Thumbnail description
            output_file: Path to save the thumbnail
        
        Returns:
            Dictionary with thumbnail generation result
        """
        try:
            # Create a colorful thumbnail for children
            width, height = 1280, 720
            image = Image.new('RGB', (width, height), color=(255, 215, 0))  # Gold background
            draw = ImageDraw.Draw(image)
            
            # Add decorative elements
            draw.rectangle([50, 50, width-50, height-50], outline=(255, 0, 0), width=5)
            
            # Try to load a font, fall back to default if unavailable
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                desc_font = ImageFont.load_default()
            
            # Add title text
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 150), title, fill=(255, 0, 0), font=title_font)
            
            # Add description text
            desc_lines = [description[i:i+30] for i in range(0, len(description), 30)]
            y_offset = 350
            for line in desc_lines[:3]:  # Max 3 lines
                draw.text((100, y_offset), line, fill=(0, 0, 0), font=desc_font)
                y_offset += 80
            
            # Save thumbnail
            image.save(output_file)
            logger.info(f"Thumbnail generated: {output_file}")
            
            return {
                "status": "success",
                "thumbnail_path": output_file
            }
        
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def convert_video_format(self, input_file: str, output_file: str, 
                            format: str = 'mp4', quality: str = '720p') -> Dict:
        """
        Convert video to desired format and quality
        
        Args:
            input_file: Path to input video
            output_file: Path for output video
            format: Video format (mp4, webm, etc.)
            quality: Video quality (360p, 480p, 720p, 1080p)
        
        Returns:
            Dictionary with conversion result
        """
        try:
            # Quality presets
            quality_presets = {
                '360p': {'bitrate': '500k', 'scale': '640:360'},
                '480p': {'bitrate': '1000k', 'scale': '854:480'},
                '720p': {'bitrate': '2500k', 'scale': '1280:720'},
                '1080p': {'bitrate': '5000k', 'scale': '1920:1080'}
            }
            
            preset = quality_presets.get(quality, quality_presets['720p'])
            
            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vf', f"scale={preset['scale']}",
                '-b:v', preset['bitrate'],
                '-c:a', 'aac',
                '-b:a', '128k',
                output_file
            ]
            
            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Video converted successfully: {output_file}")
                return {
                    "status": "success",
                    "output_file": output_file,
                    "quality": quality
                }
            else:
                logger.error(f"Conversion error: {result.stderr}")
                return {
                    "status": "error",
                    "message": result.stderr
                }
        
        except Exception as e:
            logger.error(f"Error converting video: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def add_subtitles(self, video_file: str, subtitle_file: str, output_file: str) -> Dict:
        """
        Add subtitles to a video
        
        Args:
            video_file: Path to video file
            subtitle_file: Path to subtitle file (SRT format)
            output_file: Path for output video
        
        Returns:
            Dictionary with result
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', subtitle_file,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-c:s', 'mov_text',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Subtitles added successfully: {output_file}")
                return {
                    "status": "success",
                    "output_file": output_file
                }
            else:
                logger.error(f"Subtitle error: {result.stderr}")
                return {
                    "status": "error",
                    "message": result.stderr
                }
        
        except Exception as e:
            logger.error(f"Error adding subtitles: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def trim_video(self, input_file: str, start_time: str, end_time: str, 
                   output_file: str) -> Dict:
        """
        Trim a video to specific time range
        
        Args:
            input_file: Path to input video
            start_time: Start time (HH:MM:SS)
            end_time: End time (HH:MM:SS)
            output_file: Path for output video
        
        Returns:
            Dictionary with result
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Video trimmed successfully: {output_file}")
                return {
                    "status": "success",
                    "output_file": output_file
                }
            else:
                logger.error(f"Trim error: {result.stderr}")
                return {
                    "status": "error",
                    "message": result.stderr
                }
        
        except Exception as e:
            logger.error(f"Error trimming video: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }