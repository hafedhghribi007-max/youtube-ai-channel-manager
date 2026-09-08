#!/usr/bin/env python3
"""
Complete Application Launcher
مشغل التطبيق الكامل
"""

import logging
import threading
import sys
from dashboard import DashboardApp
from discord_bot import YouTubeDiscordBot
from telegram_bot import YouTubeTelegramBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ApplicationLauncher:
    """Launch the complete YouTube AI Channel Manager application"""
    
    def __init__(self, config=None):
        self.config = config or self._load_config()
        self.modules = {}
        logger.info("Application Launcher initialized")
    
    def _load_config(self):
        """Load configuration from environment"""
        return {
            'DISCORD_BOT_TOKEN': None,
            'DISCORD_GUILD_ID': None,
            'DISCORD_CHANNEL_ID': None,
            'TELEGRAM_BOT_TOKEN': None,
            'TELEGRAM_ALLOWED_USERS': []
        }
    
    def run(self, run_dashboard=True, run_discord=False, run_telegram=False):
        """
        Run the application with selected components
        
        Args:
            run_dashboard: Run web dashboard
            run_discord: Run Discord bot
            run_telegram: Run Telegram bot
        """
        threads = []
        
        # Start Web Dashboard
        if run_dashboard:
            logger.info("Starting Web Dashboard...")
            try:
                dashboard = DashboardApp(self.modules)
                dashboard_thread = threading.Thread(
                    target=dashboard.run,
                    kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False},
                    daemon=True
                )
                dashboard_thread.start()
                threads.append(dashboard_thread)
                print("\n" + "="*60)
                print("💻 Web Dashboard: http://localhost:5000")
                print("="*60)
            except Exception as e:
                logger.error(f"Error starting dashboard: {str(e)}")
        
        # Start Discord Bot
        if run_discord and self.config.get('DISCORD_BOT_TOKEN'):
            logger.info("Starting Discord Bot...")
            try:
                discord_bot = YouTubeDiscordBot(self.config)
                discord_thread = threading.Thread(
                    target=discord_bot.run,
                    daemon=True
                )
                discord_thread.start()
                threads.append(discord_thread)
                print("🤖 Discord Bot: Connected")
            except Exception as e:
                logger.error(f"Error starting Discord bot: {str(e)}")
        
        # Start Telegram Bot
        if run_telegram and self.config.get('TELEGRAM_BOT_TOKEN'):
            logger.info("Starting Telegram Bot...")
            try:
                telegram_bot = YouTubeTelegramBot(self.config)
                telegram_thread = threading.Thread(
                    target=telegram_bot.run,
                    daemon=True
                )
                telegram_thread.start()
                threads.append(telegram_thread)
                print("📱 Telegram Bot: Connected")
            except Exception as e:
                logger.error(f"Error starting Telegram bot: {str(e)}")
        
        print("\n" + "="*60)
        print("🎬 YouTube AI Channel Manager is Running!")
        print("="*60 + "\n")
        
        # Keep the application running
        try:
            if threads:
                for thread in threads:
                    thread.join()
            else:
                print("⚠️  No components to run. Please enable at least one component.")
                sys.exit(1)
        except KeyboardInterrupt:
            logger.info("Shutting down application...")
            print("\n🛑 Application shutdown complete.")

if __name__ == '__main__':
    launcher = ApplicationLauncher()
    # Run only dashboard by default
    # To run Discord/Telegram, set their tokens in config
    launcher.run(
        run_dashboard=True,
        run_discord=False,
        run_telegram=False
    )