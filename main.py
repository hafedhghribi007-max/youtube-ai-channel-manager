#!/usr/bin/env python3
"""
YouTube AI Channel Manager - Main Application
نظام إدارة قناة يوتيوب بالذكاء الاصطناعي
"""

import sys
import logging
from flask import Flask, jsonify
from config import config
from modules.ai_content_generator import AIContentGenerator
from modules.youtube_uploader import YouTubeUploader
from modules.video_processor import VideoProcessor
from modules.analytics import AnalyticsManager
from modules.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize modules
    try:
        app.db = Database(app.config['DATABASE_URL'])
        app.ai_generator = AIContentGenerator(app.config)
        app.youtube_uploader = YouTubeUploader(app.config)
        app.video_processor = VideoProcessor(app.config)
        app.analytics = AnalyticsManager(app.config)
        logger.info("All modules initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing modules: {str(e)}")
        raise
    
    # Register routes
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy", "service": "YouTube AI Channel Manager"})
    
    @app.route('/api/generate-content', methods=['POST'])
    def generate_content():
        """Generate AI content for videos"""
        try:
            content = app.ai_generator.generate_video_idea()
            return jsonify({"status": "success", "content": content})
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/api/upload-video', methods=['POST'])
    def upload_video():
        """Upload video to YouTube"""
        try:
            result = app.youtube_uploader.upload_video()
            return jsonify({"status": "success", "result": result})
        except Exception as e:
            logger.error(f"Error uploading video: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/api/analytics', methods=['GET'])
    def get_analytics():
        """Get channel analytics"""
        try:
            analytics = app.analytics.get_channel_stats()
            return jsonify({"status": "success", "analytics": analytics})
        except Exception as e:
            logger.error(f"Error fetching analytics: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting YouTube AI Channel Manager...")
    app.run(host='0.0.0.0', port=5000, debug=True)