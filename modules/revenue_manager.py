#!/usr/bin/env python3
"""
Revenue Manager Module
مدير الأرباح
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RevenueManager:
    """Track and manage channel revenue and expenses"""
    
    def __init__(self, config):
        self.currency = config.get('CURRENCY', 'USD')
        self.adsense_enabled = config.get('ADSENSE_ENABLED', False)
        self.sponsorship_rate = config.get('SPONSORSHIP_RATE', 0.0)
        logger.info(f"RevenueManager initialized - Currency: {self.currency}")
    
    def calculate_adsense_revenue(self, views: int, cpc: float = 2.0, 
                                  ctr: float = 0.03) -> Dict:
        """
        Calculate estimated AdSense revenue
        
        Args:
            views: Number of video views
            cpc: Cost Per Click (average)
            ctr: Click-Through Rate (default 3%)
        
        Returns:
            Dictionary with revenue calculation
        """
        try:
            clicks = int(views * ctr)
            revenue = clicks * cpc
            rpm = (revenue / views * 1000) if views > 0 else 0
            
            logger.info(f"AdSense revenue calculated: ${revenue}")
            
            return {
                "status": "success",
                "views": views,
                "clicks": clicks,
                "cpc": cpc,
                "ctr": ctr,
                "revenue": round(revenue, 2),
                "rpm": round(rpm, 2),
                "currency": self.currency
            }
        
        except Exception as e:
            logger.error(f"Error calculating AdSense revenue: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def calculate_sponsorship_revenue(self, video_id: str, views: int,
                                     rate_per_1000_views: float = None) -> Dict:
        """
        Calculate sponsorship revenue
        
        Args:
            video_id: YouTube video ID
            views: Number of views
            rate_per_1000_views: Sponsorship rate per 1000 views
        
        Returns:
            Dictionary with sponsorship revenue
        """
        try:
            rate = rate_per_1000_views or self.sponsorship_rate
            revenue = (views / 1000) * rate
            
            logger.info(f"Sponsorship revenue calculated: ${revenue}")
            
            return {
                "status": "success",
                "video_id": video_id,
                "views": views,
                "rate_per_1000": rate,
                "revenue": round(revenue, 2),
                "currency": self.currency
            }
        
        except Exception as e:
            logger.error(f"Error calculating sponsorship revenue: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def calculate_total_revenue(self, video_stats: List[Dict]) -> Dict:
        """
        Calculate total revenue from all sources
        
        Args:
            video_stats: List of video statistics
        
        Returns:
            Dictionary with total revenue breakdown
        """
        try:
            total_views = 0
            total_adsense = 0
            total_sponsorship = 0
            
            for video in video_stats:
                views = video.get('views', 0)
                total_views += views
                
                # Calculate AdSense
                adsense = self.calculate_adsense_revenue(views)
                total_adsense += adsense.get('revenue', 0)
                
                # Calculate Sponsorship
                sponsorship = self.calculate_sponsorship_revenue(video.get('id'), views)
                total_sponsorship += sponsorship.get('revenue', 0)
            
            total_revenue = total_adsense + total_sponsorship
            
            logger.info(f"Total revenue calculated: ${total_revenue}")
            
            return {
                "status": "success",
                "total_views": total_views,
                "adsense_revenue": round(total_adsense, 2),
                "sponsorship_revenue": round(total_sponsorship, 2),
                "total_revenue": round(total_revenue, 2),
                "currency": self.currency
            }
        
        except Exception as e:
            logger.error(f"Error calculating total revenue: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def track_expenses(self, category: str, amount: float, 
                      description: str = '') -> Dict:
        """
        Track channel expenses
        
        Args:
            category: Expense category (equipment, software, ads, etc.)
            amount: Expense amount
            description: Expense description
        
        Returns:
            Dictionary with expense record
        """
        try:
            expense = {
                "id": hash(f"{category}{datetime.now()}"),
                "category": category,
                "amount": amount,
                "description": description,
                "date": datetime.now().isoformat(),
                "currency": self.currency
            }
            
            logger.info(f"Expense tracked: {category} - ${amount}")
            
            return {
                "status": "success",
                "expense": expense
            }
        
        except Exception as e:
            logger.error(f"Error tracking expense: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def calculate_profit(self, total_revenue: float, total_expenses: float) -> Dict:
        """
        Calculate net profit
        
        Args:
            total_revenue: Total revenue
            total_expenses: Total expenses
        
        Returns:
            Dictionary with profit calculation
        """
        try:
            profit = total_revenue - total_expenses
            profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
            
            logger.info(f"Profit calculated: ${profit}")
            
            return {
                "status": "success",
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "profit": round(profit, 2),
                "profit_margin": round(profit_margin, 2),
                "currency": self.currency
            }
        
        except Exception as e:
            logger.error(f"Error calculating profit: {str(e)}")
            return {"status": "error", "message": str(e)}