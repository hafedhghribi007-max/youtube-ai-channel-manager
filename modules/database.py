#!/usr/bin/env python3
"""
Database Module
وحدة قاعدة البيانات
"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()

class VideoContent(Base):
    """Video content model"""
    __tablename__ = 'video_contents'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    script = Column(Text)
    topic = Column(String(255))
    status = Column(String(50), default='draft')  # draft, processing, uploaded, published
    video_file_path = Column(String(500))
    thumbnail_path = Column(String(500))
    youtube_video_id = Column(String(50))
    duration = Column(Integer)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)

class UploadSchedule(Base):
    """Upload schedule model"""
    __tablename__ = 'upload_schedules'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer)
    scheduled_time = Column(DateTime, nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChannelMetrics(Base):
    """Channel metrics model"""
    __tablename__ = 'channel_metrics'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(String(50))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_rate = Column(String(10))
    recorded_at = Column(DateTime, default=datetime.utcnow)

class Database:
    """Database manager"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        logger.info("Database initialized")
    
    def add_video_content(self, title: str, description: str, script: str, 
                         topic: str, status: str = 'draft') -> dict:
        """
        Add a new video content to database
        
        Args:
            title: Video title
            description: Video description
            script: Video script
            topic: Video topic
            status: Content status
        
        Returns:
            Dictionary with result
        """
        try:
            session = self.SessionLocal()
            
            video = VideoContent(
                title=title,
                description=description,
                script=script,
                topic=topic,
                status=status
            )
            
            session.add(video)
            session.commit()
            
            logger.info(f"Video content added: {video.id}")
            return {
                "status": "success",
                "video_id": video.id
            }
        
        except Exception as e:
            logger.error(f"Error adding video content: {str(e)}")
            session.rollback()
            return {
                "status": "error",
                "message": str(e)
            }
        
        finally:
            session.close()
    
    def get_video_by_id(self, video_id: int) -> dict:
        """
        Get video content by ID
        
        Args:
            video_id: Video ID
        
        Returns:
            Dictionary with video content
        """
        try:
            session = self.SessionLocal()
            video = session.query(VideoContent).filter_by(id=video_id).first()
            
            if video:
                return {
                    "status": "success",
                    "video": {
                        "id": video.id,
                        "title": video.title,
                        "description": video.description,
                        "script": video.script,
                        "topic": video.topic,
                        "status": video.status,
                        "youtube_video_id": video.youtube_video_id,
                        "created_at": str(video.created_at)
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": "Video not found"
                }
        
        except Exception as e:
            logger.error(f"Error getting video: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
        
        finally:
            session.close()
    
    def update_video_status(self, video_id: int, status: str, 
                           youtube_video_id: str = None) -> dict:
        """
        Update video status
        
        Args:
            video_id: Video ID
            status: New status
            youtube_video_id: YouTube video ID (optional)
        
        Returns:
            Dictionary with result
        """
        try:
            session = self.SessionLocal()
            video = session.query(VideoContent).filter_by(id=video_id).first()
            
            if video:
                video.status = status
                if youtube_video_id:
                    video.youtube_video_id = youtube_video_id
                if status == 'published':
                    video.published_at = datetime.utcnow()
                
                session.commit()
                logger.info(f"Video {video_id} status updated to {status}")
                
                return {
                    "status": "success",
                    "message": f"Video status updated to {status}"
                }
            else:
                return {
                    "status": "error",
                    "message": "Video not found"
                }
        
        except Exception as e:
            logger.error(f"Error updating video status: {str(e)}")
            session.rollback()
            return {
                "status": "error",
                "message": str(e)
            }
        
        finally:
            session.close()