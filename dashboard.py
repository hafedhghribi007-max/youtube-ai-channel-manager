#!/usr/bin/env python3
"""
Web Dashboard
لوحة التحكم الويب
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from config import DevelopmentConfig

logger = logging.getLogger(__name__)

class DashboardApp:
    """Web-based dashboard for channel management"""
    
    def __init__(self, modules_dict):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        self.modules = modules_dict
        self.setup_routes()
        logger.info("Dashboard initialized")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return '''
            <!DOCTYPE html>
            <html dir="rtl" lang="ar">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>لوحة التحكم - YouTube AI Channel Manager</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .header { background: white; border-radius: 10px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
                    .header h1 { color: #333; margin-bottom: 10px; }
                    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
                    .stat-card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }
                    .stat-card .number { font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0; }
                    .stat-card .label { color: #666; font-size: 14px; }
                    .nav-tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
                    .nav-tabs button { padding: 10px 20px; background: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; transition: all 0.3s; }
                    .nav-tabs button.active { background: #667eea; color: white; }
                    .content-section { display: none; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                    .content-section.active { display: block; }
                    .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; transition: all 0.3s; }
                    .btn:hover { background: #764ba2; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📺 YouTube AI Channel Manager</h1>
                        <p>لوحة تحكم قناة يوتيوب بالذكاء الاصطناعي</p>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-card"><div class="label">📺 المشاهدات</div><div class="number" id="views-count">0</div></div>
                        <div class="stat-card"><div class="label">👍 الإعجابات</div><div class="number" id="likes-count">0</div></div>
                        <div class="stat-card"><div class="label">💬 التعليقات</div><div class="number" id="comments-count">0</div></div>
                        <div class="stat-card"><div class="label">💰 الأرباح</div><div class="number" id="revenue-count">$0</div></div>
                    </div>
                    <p style="color:white; text-align:center;">✅ لوحة التحكم نشطة وجاهزة للاستخدام!</p>
                </div>
            </body>
            </html>
            '''
        
        logger.info("Routes setup completed")
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the dashboard"""
        logger.info(f"Starting dashboard on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)