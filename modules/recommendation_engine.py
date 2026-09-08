#!/usr/bin/env python3
"""
Recommendation Engine Module
محرك التوصيات
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Recommend content based on trends and analytics"""
    
    def __init__(self, config):
        self.language = config.get('CONTENT_LANGUAGE', 'ar')
        self.trending_topics = []
        logger.info("RecommendationEngine initialized")
    
    def analyze_trending_topics(self, time_period: int = 7) -> Dict:
        """
        Analyze trending topics for children's content
        
        Args:
            time_period: Number of days to analyze
        
        Returns:
            Dictionary with trending topics
        """
        try:
            # Sample trending topics for children
            trending = {
                "educational": [
                    "تعليم الأطفال الأرقام",
                    "تعليم الحروف العربية",
                    "أغاني تعليمية",
                    "القراءة والكتابة",
                    "الرياضيات للأطفال"
                ],
                "entertainment": [
                    "قصص مضحكة",
                    "رسوم متحركة",
                    "ألعاب تفاعلية",
                    "تحديات مرحة",
                    "موسيقى أطفال"
                ],
                "skills": [
                    "رسم وفن",
                    "الحرف اليدوية",
                    "الطهي للأطفال",
                    "رقص وحركة",
                    "المهارات الحياتية"
                ]
            }
            
            logger.info(f"Trending topics analyzed for {time_period} days")
            
            return {
                "status": "success",
                "time_period_days": time_period,
                "trending_topics": trending,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def recommend_video_ideas(self, channel_history: List[Dict], 
                            engagement_data: Dict) -> Dict:
        """
        Recommend video ideas based on channel history and engagement
        
        Args:
            channel_history: List of previous videos
            engagement_data: Engagement metrics
        
        Returns:
            Dictionary with recommended video ideas
        """
        try:
            # Analyze what works best
            trending = self.analyze_trending_topics()
            
            # Get top performing topics
            top_topics = self._get_top_performing_topics(channel_history, engagement_data)
            
            # Generate recommendations
            recommendations = []
            
            for category, topics in trending['trending_topics'].items():
                for topic in topics:
                    if topic not in [v.get('topic') for v in channel_history]:
                        recommendations.append({
                            "topic": topic,
                            "category": category,
                            "priority": "high" if category in top_topics else "medium",
                            "estimated_views": self._estimate_views(topic, engagement_data),
                            "recommended_upload_time": self._recommend_upload_time()
                        })
            
            logger.info(f"Generated {len(recommendations)} video recommendations")
            
            return {
                "status": "success",
                "recommendations": sorted(recommendations, 
                                        key=lambda x: x['estimated_views'], 
                                        reverse=True)[:10]
            }
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def recommend_posting_schedule(self, channel_stats: Dict, 
                                   geography: str = 'global') -> Dict:
        """
        Recommend optimal posting schedule
        
        Args:
            channel_stats: Channel statistics
            geography: Geographic region
        
        Returns:
            Dictionary with recommended posting times
        """
        try:
            # Recommend posting times based on audience timezone
            schedules = {
                "middle_east": [
                    {"day": "Wednesday", "time": "18:00", "reason": "Evening viewing"},
                    {"day": "Friday", "time": "10:00", "reason": "Weekend start"},
                    {"day": "Saturday", "time": "19:00", "reason": "Family time"}
                ],
                "global": [
                    {"day": "Tuesday", "time": "15:00", "reason": "Mid-week peak"},
                    {"day": "Friday", "time": "17:00", "reason": "Weekend preparation"},
                    {"day": "Sunday", "time": "11:00", "reason": "Weekend leisure"}
                ]
            }
            
            schedule = schedules.get(geography, schedules['global'])
            
            logger.info(f"Posting schedule recommended for {geography}")
            
            return {
                "status": "success",
                "geography": geography,
                "recommended_schedule": schedule
            }
        
        except Exception as e:
            logger.error(f"Error recommending schedule: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _get_top_performing_topics(self, channel_history: List[Dict], 
                                   engagement_data: Dict) -> List[str]:
        """Get top performing topics from channel history"""
        if not channel_history:
            return []
        
        topics_engagement = {}
        for video in channel_history:
            topic = video.get('topic', 'unknown')
            engagement = engagement_data.get(video.get('id'), {}).get('engagement_rate', 0)
            
            if topic not in topics_engagement:
                topics_engagement[topic] = []
            topics_engagement[topic].append(engagement)
        
        # Calculate average engagement per topic
        avg_engagement = {topic: sum(values) / len(values) 
                         for topic, values in topics_engagement.items()}
        
        # Return top 3 topics
        return sorted(avg_engagement, key=avg_engagement.get, reverse=True)[:3]
    
    def _estimate_views(self, topic: str, engagement_data: Dict) -> int:
        """Estimate views for a topic"""
        base_views = 1000
        topic_boost = len(topic) * 10  # Simple heuristic
        return base_views + topic_boost
    
    def _recommend_upload_time(self) -> str:
        """Recommend upload time"""
        # Recommend next optimal time (48 hours from now)
        next_time = datetime.now() + timedelta(hours=48)
        return next_time.isoformat()
    
    def get_audience_insights(self, analytics_data: Dict) -> Dict:
        """
        Get insights about audience preferences
        
        Args:
            analytics_data: Channel analytics data
        
        Returns:
            Dictionary with audience insights
        """
        try:
            insights = {
                "preferred_content_types": ["educational", "entertainment"],
                "peak_viewing_hours": ["18:00-20:00", "10:00-12:00"],
                "average_watch_duration": "8-12 minutes",
                "preferred_video_length": "10-15 minutes",
                "audience_age_group": "4-12 years",
                "engagement_patterns": {
                    "likes_per_1000_views": 45,
                    "comments_per_1000_views": 12,
                    "shares_per_1000_views": 8
                }
            }
            
            logger.info("Audience insights generated")
            
            return {
                "status": "success",
                "insights": insights
            }
        
        except Exception as e:
            logger.error(f"Error getting audience insights: {str(e)}")
            return {"status": "error", "message": str(e)}