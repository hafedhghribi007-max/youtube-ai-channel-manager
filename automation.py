#!/usr/bin/env python3
"""
Automation Script
سكريبت الأتمتة - تشغيل المشروع بالكامل
"""

import schedule
import time
import logging
from datetime import datetime
from config import DevelopmentConfig
from modules.ai_content_generator import AIContentGenerator
from modules.youtube_uploader import YouTubeUploader
from modules.video_processor import VideoProcessor
from modules.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('channel_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ChannelAutomation:
    """Automate YouTube channel management"""
    
    def __init__(self):
        self.config = DevelopmentConfig()
        self.ai_gen = AIContentGenerator(self.config)
        self.uploader = YouTubeUploader(self.config)
        self.processor = VideoProcessor(self.config)
        self.db = Database(self.config.DATABASE_URL)
        logger.info("Channel Automation initialized")
    
    def generate_and_schedule_content(self):
        """
        Generate new content ideas and schedule them
        """
        logger.info("Generating new content...")
        
        try:
            # Generate video idea
            idea = self.ai_gen.generate_video_idea()
            
            if idea.get('status') == 'success':
                # Generate script
                script = self.ai_gen.generate_script(idea)
                
                # Save to database
                content_result = self.db.add_video_content(
                    title=f"Video - {datetime.now().strftime('%Y-%m-%d')}",
                    description=idea.get('content'),
                    script=script,
                    topic=idea.get('topic'),
                    status='draft'
                )
                
                logger.info(f"Content generated and saved: {content_result}")
            else:
                logger.error(f"Failed to generate content: {idea}")
        
        except Exception as e:
            logger.error(f"Error in content generation: {str(e)}")
    
    def start_scheduler(self):
        """
        Start the scheduling system
        """
        # Schedule content generation daily
        schedule.every().day.at("09:00").do(self.generate_and_schedule_content)
        
        logger.info("Scheduler started")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    automation = ChannelAutomation()
    logger.info("Starting Channel Automation...")
    
    # For testing, generate content immediately
    automation.generate_and_schedule_content()
    
    # Uncomment the line below to start the scheduler
    # automation.start_scheduler()