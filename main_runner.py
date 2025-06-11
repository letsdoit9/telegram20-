#!/usr/bin/env python3
"""
Main runner script for Stock Screener with Telegram Bot Integration
Supports both bot commands and daily scheduling
"""

import os
import sys
import threading
import time
from datetime import datetime
import argparse

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot
from scheduler import DailyScheduler

def run_bot_only():
    """Run only the Telegram bot (for commands)"""
    print("🤖 Starting Telegram Bot (Commands Only)")
    bot = TelegramBot()
    bot.run_bot()

def run_scheduler_only():
    """Run only the scheduler (for daily auto-messages)"""
    print("⏰ Starting Daily Scheduler")
    scheduler = DailyScheduler()
    
    try:
        # Start scheduler
        scheduler.start_scheduler()
        
        # Keep running
        while True:
            time.sleep(3600)  # Sleep for 1 hour
            print(f"💓 Scheduler running: {datetime.now()}")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop_scheduler()

def run_full_bot():
    """Run both bot and scheduler together"""
    print("🚀 Starting Full Bot (Commands + Scheduler)")
    
    # Initialize components
    bot = TelegramBot()
    scheduler = DailyScheduler()
    
    # Start scheduler in background
    scheduler.start_scheduler()
    
    # Send startup notification
    startup_message = f"""🚀 <b>FULL BOT ACTIVATED</b>
📅 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

✅ <b>Active Features:</b>
🤖 Command Bot (24/7)
⏰ Daily Scheduler (Auto-signals)
📊 Live Market Scanning
🎯 Swing Trade Analysis

💡 <b>Available Commands:</b>
/help - Show all commands
/getsignals - Get live signals
/swingtop5 - Swing criteria
/backtest - Backtesting guide

🔔 <b>Auto Schedule:</b>
9:15 AM - Market Open Alert
3:00 PM - Daily Signals  
3:30 PM - Market Close
10:00 AM (Sat) - Weekend Analysis

Ready to serve! 🎯"""
    
    bot.send_message(startup_message)
    
    try:
        # Run bot in main thread
        bot.run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Stopping full bot...")
        scheduler.stop_scheduler()
        
        # Send shutdown notification
        shutdown_message = f"""🛑 <b>BOT SHUTDOWN</b>
📅 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

❌ All automated features stopped
💡 Restart when needed

Thanks for using Stock Screener Bot! 👋"""
        
        bot.send_message(shutdown_message)

def test_connection():
    """Test Telegram connection"""
    print("🧪 Testing Telegram Connection...")
    
    bot = TelegramBot()
    test_message = f"🧪 <b>CONNECTION TEST</b>\n📅 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n✅ Bot is working correctly!"
    
    if bot.send_message(test_message):
        print("✅ Telegram connection successful!")
        return True
    else:
        print("❌ Telegram connection failed!")
        return False

def show_status():
    """Show current configuration status"""
    print("\n📊 CONFIGURATION STATUS")
    print("=" * 50)
    
    # Check environment variables
    access_token = os.getenv('UPSTOX_ACCESS_TOKEN', '')
    print(f"🔑 UPSTOX_ACCESS_TOKEN: {'✅ Set' if access_token else '❌ Not Set'}")
    
    # Check bot token (from script)
    try:
        from telegram_bot import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
        print(f"🤖 TELEGRAM_BOT_TOKEN: {'✅ Set' if TELEGRAM_BOT_TOKEN else '❌ Not Set'}")
        print(f"💬 TELEGRAM_CHAT_ID: {'✅ Set' if TELEGRAM_CHAT_ID else '❌ Not Set'}")
    except ImportError:
        print("❌ telegram_bot.py not found or has errors")
    
    # Check CSV file
    csv_exists = os.path.exists('nifty500_instrument_keys.csv')
    print(f"📁 nifty500_instrument_keys.csv: {'✅ Found' if csv_exists else '❌ Missing'}")
    
    # Check other required files
    files_to_check = ['telegram_bot.py', 'scheduler.py', 'streamlit_app.py', 'requirements.txt']
    for file in files_to_check:
        exists = os.path.exists(file)
        print(f"📄 {file}: {'✅ Found' if exists else '❌ Missing'}")
    
    print("\n💡 SETUP INSTRUCTIONS:")
    if not access_token:
        print("   • Set UPSTOX_ACCESS_TOKEN: export UPSTOX_ACCESS_TOKEN='your_token'")
    if not csv_exists:
        print("   • Add nifty500_instrument_keys.csv file")
    
    print("\n🚀 READY TO RUN!" if (access_token and csv_exists) else "\n⚠️  SETUP REQUIRED")

def setup_guide():
    """Show detailed setup guide"""
    print("""
🔧 DETAILED SETUP GUIDE
====================

📋 Prerequisites:
1. Python 3.8+ installed
2. Upstox API access token
3. Telegram bot token & chat ID
4. Required CSV file (nifty500_instrument_keys.csv)

📝 Step-by-Step Setup:

1️⃣ Install Dependencies:
   pip install -r requirements.txt

2️⃣ Set Environment Variables:
   • Windows: set UPSTOX_ACCESS_TOKEN=your_token_here
   • Linux/Mac: export UPSTOX_ACCESS_TOKEN=your_token_here

3️⃣ Update telegram_bot.py:
   • Add your TELEGRAM_BOT_TOKEN
   • Add your TELEGRAM_CHAT_ID

4️⃣ Add CSV File:
   • Place nifty500_instrument_keys.csv in project folder

5️⃣ Test Connection:
   python main_runner.py --test

6️⃣ Run Bot:
   • Bot Only: python main_runner.py --bot
   • Scheduler Only: python main_runner.py --scheduler
   • Full Bot: python main_runner.py --full

🎯 Ready to use!
""")

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='Stock Screener Telegram Bot')
    
    parser.add_argument('--bot', action='store_true', 
                       help='Run only Telegram bot (commands)')
    parser.add_argument('--scheduler', action='store_true', 
                       help='Run only scheduler (auto messages)')
    parser.add_argument('--full', action='store_true', 
                       help='Run both bot and scheduler')
    parser.add_argument('--test', action='store_true', 
                       help='Test Telegram connection')
    parser.add_argument('--status', action='store_true', 
                       help='Show configuration status')
    parser.add_argument('--setup', action='store_true', 
                       help='Show setup guide')
    
    args = parser.parse_args()
    
    # Show header
    print("\n" + "="*60)
    print("🎯 STOCK SCREENER TELEGRAM BOT")
    print("="*60)
    
    try:
        if args.test:
            test_connection()
        elif args.status:
            show_status()
        elif args.setup:
            setup_guide()
        elif args.bot:
            run_bot_only()
        elif args.scheduler:
            run_scheduler_only()
        elif args.full:
            run_full_bot()
        else:
            # Default behavior - show help
            print("""
🚀 AVAILABLE MODES:

🤖 Bot Commands:
   python main_runner.py --bot        # Run command bot only
   python main_runner.py --scheduler  # Run scheduler only  
   python main_runner.py --full       # Run both together

🔧 Setup & Testing:
   python main_runner.py --test       # Test connection
   python main_runner.py --status     # Check config
   python main_runner.py --setup      # Setup guide

💡 Example Usage:
   python main_runner.py --full       # Most common usage
   
Choose your mode and run! 🎯
""")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Try: python main_runner.py --status")
        sys.exit(1)

if __name__ == "__main__":
    main()