#!/usr/bin/env python3
"""
AI Content Generator Module
مولد المحتوى بالذكاء الاصطناعي
"""

import openai
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AIContentGenerator:
    """Generate video content ideas and scripts using AI"""
    
    def __init__(self, config):
        self.api_key = config.get('OPENAI_API_KEY')
        self.language = config.get('CONTENT_LANGUAGE', 'ar')
        self.audience = config.get('TARGET_AUDIENCE', 'children')
        openai.api_key = self.api_key
        logger.info(f"AIContentGenerator initialized for {self.audience} audience in {self.language}")
    
    def generate_video_idea(self, topic: Optional[str] = None) -> Dict:
        """
        Generate a creative video idea for children
        
        Args:
            topic: Optional specific topic to generate ideas for
        
        Returns:
            Dictionary containing video title, description, and script ideas
        """
        try:
            prompt = f"""
            Generate a creative and educational video idea for children (ages 4-12).
            The content should be:
            - Age-appropriate and safe
            - Educational and entertaining
            - In {self.language} language
            - Engaging and fun
            
            {'Topic: ' + topic if topic else 'Generate a random topic'}
            
            Please provide:
            1. Video Title
            2. Video Description (2-3 sentences)
            3. Key Learning Points (3-4 points)
            4. Script Outline (5-7 key scenes)
            5. Suggested Background Music Style
            6. Props/Resources Needed
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative content director for children's educational videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            logger.info("Video idea generated successfully")
            
            return {
                "status": "success",
                "content": content,
                "topic": topic or "Random",
                "language": self.language
            }
        
        except Exception as e:
            logger.error(f"Error generating video idea: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def generate_script(self, video_idea: Dict) -> str:
        """
        Generate a detailed script from a video idea
        
        Args:
            video_idea: Dictionary containing the video concept
        
        Returns:
            Detailed video script
        """
        try:
            prompt = f"""
            Create a detailed, engaging script for a children's video based on this idea:
            {video_idea.get('content', '')}
            
            The script should:
            - Be clear and easy to follow
            - Include dialogue and narration
            - Have timing information for each scene
            - Include visual descriptions
            - Be appropriate for ages 4-12
            - Be in {self.language} language
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert scriptwriter for children's educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2000
            )
            
            script = response.choices[0].message.content
            logger.info("Script generated successfully")
            return script
        
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_thumbnail_description(self, video_title: str) -> Dict:
        """
        Generate thumbnail and title suggestions
        
        Args:
            video_title: The title of the video
        
        Returns:
            Dictionary with thumbnail descriptions and design suggestions
        """
        try:
            prompt = f"""
            Create a detailed description for YouTube thumbnail design for this video:
            Title: {video_title}
            
            Provide:
            1. Main visual elements (what should be the focus)
            2. Color scheme recommendations (bright and appealing for children)
            3. Text overlay suggestions
            4. Key colors to use
            5. Composition tips
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert YouTube thumbnail designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            description = response.choices[0].message.content
            logger.info("Thumbnail description generated")
            
            return {
                "status": "success",
                "thumbnail_description": description
            }
        
        except Exception as e:
            logger.error(f"Error generating thumbnail description: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }