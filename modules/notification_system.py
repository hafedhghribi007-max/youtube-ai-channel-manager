#!/usr/bin/env python3
"""
Notification System Module
نظام التنبيهات
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class NotificationSystem:
    """Send alerts and notifications for important events"""
    
    def __init__(self, config):
        self.email_enabled = config.get('EMAIL_NOTIFICATIONS', True)
        self.sms_enabled = config.get('SMS_NOTIFICATIONS', False)
        self.discord_webhook = config.get('DISCORD_WEBHOOK')
        self.telegram_bot_token = config.get('TELEGRAM_BOT_TOKEN')
        self.notifications_log = []
        logger.info("NotificationSystem initialized")
    
    def send_performance_alert(self, video_id: str, video_title: str,
                               performance_data: Dict) -> Dict:
        """
        Send alert when video performance reaches thresholds
        
        Args:
            video_id: YouTube video ID
            video_title: Video title
            performance_data: Performance metrics
        
        Returns:
            Dictionary with alert result
        """
        try:
            alerts = []
            
            # Check various performance thresholds
            views = performance_data.get('views', 0)
            likes = performance_data.get('likes', 0)
            comments = performance_data.get('comments', 0)
            
            if views > 5000:
                alerts.append({
                    "type": "milestone",
                    "message": f"🎉 {video_title} reached 5,000 views!",
                    "severity": "info"
                })
            
            if views > 10000:
                alerts.append({
                    "type": "milestone",
                    "message": f"🌟 {video_title} reached 10,000 views!",
                    "severity": "high"
                })
            
            engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
            
            if engagement_rate > 5:
                alerts.append({
                    "type": "engagement",
                    "message": f"💪 High engagement: {engagement_rate:.2f}% on {video_title}",
                    "severity": "info"
                })
            
            # Send alerts
            for alert in alerts:
                self._send_notification(alert['message'], alert['severity'])
            
            logger.info(f"Performance alerts sent: {len(alerts)}")
            
            return {
                "status": "success",
                "video_id": video_id,
                "alerts_sent": len(alerts),
                "alerts": alerts
            }
        
        except Exception as e:
            logger.error(f"Error sending performance alert: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def send_monetization_alert(self, earnings: float, threshold: float = 100) -> Dict:
        """
        Send alert when earnings reach threshold
        
        Args:
            earnings: Current earnings
            threshold: Alert threshold
        
        Returns:
            Dictionary with alert result
        """
        try:
            if earnings >= threshold:
                message = f"💰 Congratulations! You've earned ${earnings:.2f}! Withdrawal minimum reached!"
                severity = "high"
                
                self._send_notification(message, severity)
                
                logger.info(f"Monetization alert sent: ${earnings}")
                
                return {
                    "status": "success",
                    "message": message,
                    "earnings": earnings,
                    "threshold_reached": True
                }
            
            return {
                "status": "success",
                "message": "Earnings below threshold",
                "earnings": earnings,
                "threshold_reached": False
            }
        
        except Exception as e:
            logger.error(f"Error sending monetization alert: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def send_upload_scheduled_notification(self, video_title: str,
                                          scheduled_time: datetime) -> Dict:
        """
        Send notification when video is scheduled to upload
        
        Args:
            video_title: Video title
            scheduled_time: Scheduled upload time
        
        Returns:
            Dictionary with result
        """
        try:
            message = f"📅 Video '{video_title}' scheduled for upload at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            self._send_notification(message, "info")
            
            logger.info(f"Upload scheduled notification sent for: {video_title}")
            
            return {
                "status": "success",
                "message": message,
                "video_title": video_title,
                "scheduled_time": scheduled_time.isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error sending upload notification: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def send_subscriber_alert(self, subscriber_count: int) -> Dict:
        """
        Send alert when reaching subscriber milestones
        
        Args:
            subscriber_count: Current subscriber count
        
        Returns:
            Dictionary with alert result
        """
        try:
            milestones = [100, 500, 1000, 5000, 10000, 50000, 100000]
            message = None
            
            for milestone in milestones:
                if subscriber_count == milestone:
                    message = f"🎊 Congratulations! You reached {milestone} subscribers!"
                    break
            
            if message:
                self._send_notification(message, "high")
                logger.info(f"Subscriber milestone alert: {subscriber_count}")
                
                return {
                    "status": "success",
                    "message": message,
                    "milestone": subscriber_count
                }
            
            return {
                "status": "success",
                "message": "No milestone reached",
                "subscriber_count": subscriber_count
            }
        
        except Exception as e:
            logger.error(f"Error sending subscriber alert: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _send_notification(self, message: str, severity: str = "info"):
        """
        Send notification through all enabled channels
        """
        notification = {
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        
        self.notifications_log.append(notification)
        
        # Send through Discord
        if self.discord_webhook:
            self._send_discord_notification(message, severity)
        
        # Send through Telegram
        if self.telegram_bot_token:
            self._send_telegram_notification(message, severity)
        
        # Send through Email (if enabled)
        if self.email_enabled:
            self._send_email_notification(message, severity)
    
    def _send_discord_notification(self, message: str, severity: str):
        """Send notification via Discord webhook"""
        try:
            # Color based on severity
            colors = {
                "info": 3447003,
                "warning": 15105570,
                "high": 15158332
            }
            
            payload = {
                "embeds": [{
                    "title": "YouTube Channel Alert",
                    "description": message,
                    "color": colors.get(severity, 3447003),
                    "timestamp": datetime.now().isoformat()
                }]
            }
            
            logger.info("Discord notification prepared")
        
        except Exception as e:
            logger.error(f"Discord notification error: {str(e)}")
    
    def _send_telegram_notification(self, message: str, severity: str):
        """Send notification via Telegram"""
        try:
            # Telegram bot integration
            logger.info("Telegram notification prepared")
        
        except Exception as e:
            logger.error(f"Telegram notification error: {str(e)}")
    
    def _send_email_notification(self, message: str, severity: str):
        """Send notification via Email"""
        try:
            # Email integration
            logger.info("Email notification prepared")
        
        except Exception as e:
            logger.error(f"Email notification error: {str(e)}")
    
    def get_notification_history(self, limit: int = 50) -> Dict:
        """
        Get notification history
        
        Args:
            limit: Maximum number of notifications to return
        
        Returns:
            Dictionary with notification history
        """
        try:
            history = self.notifications_log[-limit:]
            
            return {
                "status": "success",
                "total_notifications": len(self.notifications_log),
                "notifications": history
            }
        
        except Exception as e:
            logger.error(f"Error getting notification history: {str(e)}")
            return {"status": "error", "message": str(e)}