#!/usr/bin/env python3
"""
AI Image Generator Module
مولد الصور بالذكاء الاصطناعي
"""

import logging
import requests
from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

logger = logging.getLogger(__name__)

class AIImageGenerator:
    """Generate AI-powered images and animations"""
    
    def __init__(self, config):
        self.api_key = config.get('OPENAI_API_KEY')
        self.output_dir = 'generated_images'
        logger.info("AIImageGenerator initialized")
    
    def generate_thumbnail_ai(self, video_title: str, theme: str = 'colorful') -> Dict:
        """
        Generate AI-powered thumbnail using DALL-E
        
        Args:
            video_title: Title for the thumbnail
            theme: Color theme (colorful, dark, bright, etc.)
        
        Returns:
            Dictionary with image URL and metadata
        """
        try:
            prompt = f"""
            Create a vibrant, eye-catching YouTube thumbnail for children's content.
            Title: {video_title}
            Style: {theme}
            Requirements:
            - Bright and appealing colors
            - Simple, clear design
            - Safe for children
            - Professional quality
            - 16:9 aspect ratio
            """
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'prompt': prompt,
                    'n': 1,
                    'size': '1280x720',
                    'quality': 'hd'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['data'][0]['url']
                logger.info(f"Thumbnail generated: {image_url}")
                return {
                    "status": "success",
                    "image_url": image_url,
                    "title": video_title
                }
            else:
                logger.error(f"API error: {response.text}")
                return {"status": "error", "message": response.text}
        
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def create_animated_thumbnail(self, base_image_path: str, text: str, 
                                 output_file: str, animation_frames: int = 10) -> Dict:
        """
        Create animated thumbnail with text overlay
        
        Args:
            base_image_path: Path to base image
            text: Text to overlay
            output_file: Output GIF file path
            animation_frames: Number of animation frames
        
        Returns:
            Dictionary with result
        """
        try:
            base_image = Image.open(base_image_path)
            frames = []
            
            for i in range(animation_frames):
                frame = base_image.copy()
                draw = ImageDraw.Draw(frame)
                
                # Animated text position
                y_pos = 50 + (i * 3)
                
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
                except:
                    font = ImageFont.load_default()
                
                # Draw text with shadow effect
                draw.text((y_pos, y_pos), text, fill=(255, 255, 255), font=font)
                draw.text((y_pos+2, y_pos+2), text, fill=(0, 0, 0), font=font)
                
                frames.append(frame)
            
            # Save as animated GIF
            frames[0].save(
                output_file,
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0
            )
            
            logger.info(f"Animated thumbnail created: {output_file}")
            return {
                "status": "success",
                "output_file": output_file,
                "frames": animation_frames
            }
        
        except Exception as e:
            logger.error(f"Error creating animated thumbnail: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def generate_brand_colors(self, channel_name: str) -> Dict:
        """
        Generate brand colors palette for channel
        
        Args:
            channel_name: Name of the channel
        
        Returns:
            Dictionary with color palette
        """
        try:
            # Generate a unique color palette based on channel name
            colors = self._generate_color_palette(channel_name)
            logger.info(f"Brand colors generated for {channel_name}")
            
            return {
                "status": "success",
                "channel_name": channel_name,
                "primary_color": colors['primary'],
                "secondary_color": colors['secondary'],
                "accent_color": colors['accent'],
                "palette": colors['palette']
            }
        
        except Exception as e:
            logger.error(f"Error generating brand colors: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_color_palette(self, seed_text: str) -> Dict:
        """Generate color palette from seed text"""
        # Convert text to hash for consistent colors
        hash_value = hash(seed_text) % 0xFFFFFF
        
        primary = f'#{hash_value:06x}'
        secondary = f'#{(hash_value ^ 0x555555):06x}'
        accent = f'#{(hash_value ^ 0xAAAAAA):06x}'
        
        palette = [primary, secondary, accent]
        for i in range(2):
            palette.append(f'#{(hash_value ^ (i * 0x333333)):06x}')
        
        return {
            'primary': primary,
            'secondary': secondary,
            'accent': accent,
            'palette': palette
        }