#!/usr/bin/env python3
"""
Analytics Manager Module
مدير التحليلات
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

class AnalyticsManager:
    """Manage channel analytics and performance tracking"""
    
    def __init__(self, config):
        self.api_key = config.get('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        logger.info("AnalyticsManager initialized")
    
    def get_channel_stats(self) -> Dict:
        """
        Get channel statistics
        
        Returns:
            Dictionary with channel stats (subscribers, views, video count)
        """
        try:
            request = self.youtube.channels().list(
                part='statistics,snippet',
                mine=True
            )
            
            response = request.execute()
            
            if response.get('items'):
                channel = response['items'][0]
                stats = channel.get('statistics', {})
                snippet = channel.get('snippet', {})
                
                return {
                    "status": "success",
                    "channel_name": snippet.get('title'),
                    "subscribers": stats.get('subscriberCount', 'Not disclosed'),
                    "view_count": stats.get('viewCount', 0),
                    "video_count": stats.get('videoCount', 0),
                    "description": snippet.get('description')
                }
            else:
                return {
                    "status": "error",
                    "message": "Channel not found"
                }
        
        except Exception as e:
            logger.error(f"Error getting channel stats: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_video_analytics(self, video_id: str) -> Dict:
        """
        Get analytics for a specific video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with video statistics
        """
        try:
            request = self.youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            )
            
            response = request.execute()
            
            if response.get('items'):
                video = response['items'][0]
                stats = video.get('statistics', {})
                snippet = video.get('snippet', {})
                
                return {
                    "status": "success",
                    "video_id": video_id,
                    "title": snippet.get('title'),
                    "view_count": int(stats.get('viewCount', 0)),
                    "like_count": int(stats.get('likeCount', 0)),
                    "comment_count": int(stats.get('commentCount', 0)),
                    "published_at": snippet.get('publishedAt')
                }
            else:
                return {
                    "status": "error",
                    "message": "Video not found"
                }
        
        except Exception as e:
            logger.error(f"Error getting video analytics: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_channel_videos(self, max_results: int = 50) -> Dict:
        """
        Get list of channel videos with stats
        
        Args:
            max_results: Maximum number of results
        
        Returns:
            Dictionary with list of videos and their stats
        """
        try:
            # First, get the channel ID
            channel_request = self.youtube.channels().list(
                part='contentDetails',
                mine=True
            )
            channel_response = channel_request.execute()
            
            if not channel_response.get('items'):
                return {"status": "error", "message": "Channel not found"}
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=min(max_results, 50)
            )
            
            playlist_response = playlist_request.execute()
            
            videos = []
            for item in playlist_response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                video_stats = self.get_video_analytics(video_id)
                videos.append(video_stats)
            
            return {
                "status": "success",
                "total_videos": len(videos),
                "videos": videos
            }
        
        except Exception as e:
            logger.error(f"Error getting channel videos: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def calculate_engagement_rate(self, video_id: str) -> Dict:
        """
        Calculate engagement rate for a video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with engagement metrics
        """
        try:
            video_stats = self.get_video_analytics(video_id)
            
            if video_stats.get('status') != 'success':
                return video_stats
            
            views = video_stats.get('view_count', 1)
            likes = video_stats.get('like_count', 0)
            comments = video_stats.get('comment_count', 0)
            
            engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
            
            return {
                "status": "success",
                "video_id": video_id,
                "views": views,
                "engagement_rate": round(engagement_rate, 2),
                "like_rate": round((likes / views * 100), 2) if views > 0 else 0,
                "comment_rate": round((comments / views * 100), 2) if views > 0 else 0
            }
        
        except Exception as e:
            logger.error(f"Error calculating engagement rate: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }