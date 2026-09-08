import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///youtube_channel.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    TARGET_AUDIENCE = os.getenv('TARGET_AUDIENCE', 'children')
    CONTENT_LANGUAGE = os.getenv('CONTENT_LANGUAGE', 'ar')
    VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', '720p')
    UPLOAD_SCHEDULE = os.getenv('UPLOAD_SCHEDULE', 'daily')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}