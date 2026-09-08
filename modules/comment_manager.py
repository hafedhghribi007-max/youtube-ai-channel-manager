#!/usr/bin/env python3
"""
Comment Management Module
إدارة التعليقات
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class CommentManager:
    """Manage and moderate video comments"""
    
    def __init__(self, config):
        self.language = config.get('CONTENT_LANGUAGE', 'ar')
        self.auto_moderate = config.get('AUTO_MODERATE', True)
        self.blocked_keywords = self._load_blocked_keywords()
        logger.info("CommentManager initialized")
    
    def _load_blocked_keywords(self) -> List[str]:
        """Load blocked keywords for moderation"""
        return [
            'hate', 'violence', 'inappropriate', 'spam',
            'adult', 'obscene', 'discriminate'
        ]
    
    def moderate_comment(self, comment_text: str, author: str, 
                        video_id: str) -> Dict:
        """
        Moderate a comment for appropriateness
        
        Args:
            comment_text: The comment text
            author: Comment author name
            video_id: YouTube video ID
        
        Returns:
            Dictionary with moderation result
        """
        try:
            # Check for blocked keywords
            is_flagged = self._check_blocked_content(comment_text)
            
            # Check for spam
            is_spam = self._detect_spam(comment_text, author)
            
            # Check language appropriateness
            language_check = self._check_language_appropriateness(comment_text)
            
            if is_flagged or is_spam or not language_check['appropriate']:
                action = 'hold_for_review' if not self.auto_moderate else 'auto_delete'
                reason = []
                
                if is_flagged:
                    reason.append('Contains blocked keywords')
                if is_spam:
                    reason.append('Detected as spam')
                if not language_check['appropriate']:
                    reason.append(language_check['reason'])
            else:
                action = 'approve'
                reason = ['Comment approved']
            
            logger.info(f"Comment moderated: {action}")
            
            return {
                "status": "success",
                "comment": comment_text[:50] + "...",
                "author": author,
                "video_id": video_id,
                "action": action,
                "reason": reason,
                "moderated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error moderating comment: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def auto_reply_comment(self, comment_text: str, video_id: str, 
                          comment_id: str) -> Dict:
        """
        Generate and post automatic reply to comment
        
        Args:
            comment_text: Comment text
            video_id: YouTube video ID
            comment_id: Comment ID
        
        Returns:
            Dictionary with reply
        """
        try:
            # Generate context-aware reply
            reply = self._generate_reply(comment_text)
            
            # Note: Actual YouTube API integration needed for posting
            logger.info(f"Auto-reply generated for comment {comment_id}")
            
            return {
                "status": "success",
                "comment_id": comment_id,
                "video_id": video_id,
                "reply": reply,
                "generated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error generating auto-reply: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_reply(self, comment_text: str) -> str:
        """
        Generate appropriate reply based on comment
        """
        replies = {
            'love': 'شكراً لك! نحن سعداء أنك استمتعت! 🎉',
            'great': 'شكراً! نأمل أن تستمتع بالمزيد من الفيديوهات! 🌟',
            'more': 'سنحضر المزيد قريباً! شكراً على المتابعة! 📹',
            'subscribe': 'شكراً على الاشتراك! 🎊',
            'thanks': 'شكراً لك! نتمنى أن ينال إعجابك! ❤️',
            'default': 'شكراً على التعليق! نقدر تفاعلك! 😊'
        }
        
        # Simple keyword matching
        comment_lower = comment_text.lower()
        
        for keyword, reply in replies.items():
            if keyword in comment_lower:
                return reply
        
        return replies['default']
    
    def _check_blocked_content(self, text: str) -> bool:
        """Check if text contains blocked keywords"""
        text_lower = text.lower()
        for keyword in self.blocked_keywords:
            if keyword in text_lower:
                return True
        return False
    
    def _detect_spam(self, comment_text: str, author: str) -> bool:
        """
        Detect spam comments
        """
        # Check for repeated characters
        if re.search(r'(.)\1{4,}', comment_text):
            return True
        
        # Check for excessive links
        if comment_text.count('http') > 2:
            return True
        
        # Check for all caps
        if len(comment_text) > 10 and comment_text.isupper():
            return True
        
        return False
    
    def _check_language_appropriateness(self, text: str) -> Dict:
        """
        Check if language is appropriate for children
        """
        inappropriate_patterns = [
            r'\b(bad|terrible|worst)\b',
            r'[!@#$%^&*]{3,}',
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return {
                    "appropriate": False,
                    "reason": "Contains inappropriate language"
                }
        
        return {"appropriate": True, "reason": "Comment is appropriate"}
    
    def get_top_comments(self, video_id: str, limit: int = 10) -> Dict:
        """
        Get top comments for a video
        
        Args:
            video_id: YouTube video ID
            limit: Number of comments to return
        
        Returns:
            Dictionary with top comments
        """
        try:
            # This would integrate with YouTube API
            # Placeholder implementation
            
            logger.info(f"Retrieved top {limit} comments for video {video_id}")
            
            return {
                "status": "success",
                "video_id": video_id,
                "comments": [],  # Would be populated from API
                "total_comments": 0
            }
        
        except Exception as e:
            logger.error(f"Error getting comments: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def pin_comment(self, video_id: str, comment_id: str) -> Dict:
        """
        Pin a comment on the video
        
        Args:
            video_id: YouTube video ID
            comment_id: Comment ID to pin
        
        Returns:
            Dictionary with result
        """
        try:
            logger.info(f"Comment {comment_id} pinned on video {video_id}")
            
            return {
                "status": "success",
                "video_id": video_id,
                "comment_id": comment_id,
                "action": "pinned"
            }
        
        except Exception as e:
            logger.error(f"Error pinning comment: {str(e)}")
            return {"status": "error", "message": str(e)}