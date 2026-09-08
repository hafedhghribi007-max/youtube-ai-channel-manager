#!/usr/bin/env python3
"""
YouTube Uploader Module
وحدة تحميل الفيديوهات على يوتيوب
"""

import logging
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class YouTubeUploader:
    """Upload videos to YouTube channel"""
    
    # YouTube API scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, config):
        self.api_key = config.get('YOUTUBE_API_KEY')
        self.client_id = config.get('YOUTUBE_CLIENT_ID')
        self.client_secret = config.get('YOUTUBE_CLIENT_SECRET')
        self.youtube = None
        self._authenticate()
        logger.info("YouTubeUploader initialized")
    
    def _authenticate(self):
        """
        Authenticate with YouTube API
        """
        try:
            credentials = None
            
            # Check if token.pickle exists
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    credentials = Credentials.from_authorized_user_file('token.pickle')
            
            # If no credentials, authenticate with OAuth flow
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    credentials = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open('token.pickle', 'wb') as token:
                    import pickle
                    pickle.dump(credentials, token)
            
            self.youtube = build('youtube', 'v3', credentials=credentials)
            logger.info("YouTube authentication successful")
        
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise
    
    def upload_video(self, video_file: str, title: str, description: str, 
                     tags: list, category_id: str = '22') -> Dict:
        """
        Upload a video to YouTube
        
        Args:
            video_file: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags/keywords
            category_id: YouTube category ID (22 = Short Movies, 23 = Animation for kids)
        
        Returns:
            Dictionary with upload result
        """
        try:
            if not os.path.exists(video_file):
                raise FileNotFoundError(f"Video file not found: {video_file}")
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': 'private',  # Set to private initially
                    'madeForKids': True  # Important for children's content
                }
            }
            
            media = MediaFileUpload(
                video_file,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                try:
                    status, response = request.next_chunk()
                    if status:
                        logger.info(f"Upload progress: {int(status.progress() * 100)}%")
                except Exception as e:
                    logger.error(f"Upload error: {str(e)}")
                    raise
            
            video_id = response.get('id')
            logger.info(f"Video uploaded successfully: {video_id}")
            
            return {
                "status": "success",
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }
        
        except Exception as e:
            logger.error(f"Error uploading video: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def set_video_public(self, video_id: str) -> Dict:
        """
        Make a video public
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with result
        """
        try:
            request = self.youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': 'public'
                    }
                }
            )
            
            response = request.execute()
            logger.info(f"Video {video_id} set to public")
            
            return {
                "status": "success",
                "message": "Video is now public"
            }
        
        except Exception as e:
            logger.error(f"Error setting video public: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_playlist(self, title: str, description: str) -> Dict:
        """
        Create a new playlist
        
        Args:
            title: Playlist title
            description: Playlist description
        
        Returns:
            Dictionary with playlist ID
        """
        try:
            request = self.youtube.playlists().insert(
                part='snippet',
                body={
                    'snippet': {
                        'title': title,
                        'description': description
                    }
                }
            )
            
            response = request.execute()
            playlist_id = response.get('id')
            logger.info(f"Playlist created: {playlist_id}")
            
            return {
                "status": "success",
                "playlist_id": playlist_id
            }
        
        except Exception as e:
            logger.error(f"Error creating playlist: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }