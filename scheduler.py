import schedule
import time
import threading
from datetime import datetime, timedelta
import pytz
from telegram_bot import TelegramBot

class DailyScheduler:
    def __init__(self):
        self.bot = TelegramBot()
        self.is_running = False
        self.scheduler_thread = None
        
        # Indian timezone
        self.ist = pytz.timezone('Asia/Kolkata')
    
    def is_market_day(self):
        """Check if today is a market day (Monday to Friday, excluding holidays)"""
        today = datetime.now(self.ist)
        
        # Check if it's a weekday (Monday=0, Sunday=6)
        if today.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Basic holiday check (you can expand this)
        # Indian market holidays - add more as needed
        holidays_2024 = [
            '2024-01-26',  # Republic Day
            '2024-03-08',  # Holi
            '2024-03-29',  # Good Friday
            '2024-04-11',  # Eid ul Fitr
            '2024-04-17',  # Ram Navami
            '2024-05-01',  # Maharashtra Day
            '2024-06-17',  # Eid ul Adha
            '2024-08-15',  # Independence Day
            '2024-08-26',  # Janmashtami
            '2024-10-02',  # Gandhi Jayanti
            '2024-10-31',  # Diwali Laxmi Puja
            '2024-11-01',  # Diwali Balipratipada
            '2024-11-15',  # Guru Nanak Jayanti
            '2024-12-25',  # Christmas
        ]
        
        today_str = today.strftime('%Y-%m-%d')
        return today_str not in holidays_2024
    
    def send_market_open_message(self):
        """Send market open message"""
        if not self.is_market_day():
            return
        
        message = f"""🌅 <b>MARKET OPEN</b>
📅 {datetime.now(self.ist).strftime('%A, %B %d, %Y')}
🕘 {datetime.now(self.ist).strftime('%H:%M IST')}

🚀 Markets are now open!
💡 Use /getsignals for fresh opportunities
📊 Daily signals coming at 3:00 PM

Good luck trading! 📈"""
        
        self.bot.send_message(message)
        print(f"✅ Market open message sent at {datetime.now(self.ist)}")
    
    def send_daily_signals(self):
        """Send daily signals"""
        if not self.is_market_day():
            return
        
        print(f"🔄 Running daily signals at {datetime.now(self.ist)}")
        self.bot.send_daily_signals()
        print(f"✅ Daily signals completed at {datetime.now(self.ist)}")
    
    def send_market_close_message(self):
        """Send market close message"""
        if not self.is_market_day():
            return
        
        message = f"""🌇 <b>MARKET CLOSED</b>
📅 {datetime.now(self.ist).strftime('%A, %B %d, %Y')}
🕘 {datetime.now(self.ist).strftime('%H:%M IST')}

📊 Trading session ended
💼 Time to review your trades
📈 Prepare for tomorrow's opportunities

Have a great evening! 🌟"""
        
        self.bot.send_message(message)
        print(f"✅ Market close message sent at {datetime.now(self.ist)}")
    
    def send_weekend_analysis(self):
        """Send weekend market analysis"""
        message = f"""📊 <b>WEEKEND MARKET ANALYSIS</b>
📅 {datetime.now(self.ist).strftime('%A, %B %d, %Y')}

🔍 <b>This Week's Performance:</b>
• Markets closed for the weekend
• Time for portfolio review
• Plan next week's strategies

📈 <b>Next Week Preparation:</b>
• Review global cues
• Check earnings calendar
• Identify sector trends
• Update watchlists

💡 <b>Weekend Tasks:</b>
• Analyze your trades
• Study new setups
• Read market news
• Practice backtesting

Use /backtest for detailed guidance!

Happy Weekend! 🎉"""
        
        self.bot.send_message(message)
        print(f"✅ Weekend analysis sent at {datetime.now(self.ist)}")
    
    def schedule_jobs(self):
        """Schedule all jobs"""
        # Market open message (9:15 AM IST)
        schedule.every().monday.at("09:15").do(self.send_market_open_message)
        schedule.every().tuesday.at("09:15").do(self.send_market_open_message)
        schedule.every().wednesday.at("09:15").do(self.send_market_open_message)
        schedule.every().thursday.at("09:15").do(self.send_market_open_message)
        schedule.every().friday.at("09:15").do(self.send_market_open_message)
        
        # Daily signals (3:00 PM IST)
        schedule.every().monday.at("15:00").do(self.send_daily_signals)
        schedule.every().tuesday.at("15:00").do(self.send_daily_signals)
        schedule.every().wednesday.at("15:00").do(self.send_daily_signals)
        schedule.every().thursday.at("15:00").do(self.send_daily_signals)
        schedule.every().friday.at("15:00").do(self.send_daily_signals)
        
        # Market close message (3:30 PM IST)
        schedule.every().monday.at("15:30").do(self.send_market_close_message)
        schedule.every().tuesday.at("15:30").do(self.send_market_close_message)
        schedule.every().wednesday.at("15:30").do(self.send_market_close_message)
        schedule.every().thursday.at("15:30").do(self.send_market_close_message)
        schedule.every().friday.at("15:30").do(self.send_market_close_message)
        
        # Weekend analysis (Saturday 10:00 AM IST)
        schedule.every().saturday.at("10:00").do(self.send_weekend_analysis)
        
        print("📅 All jobs scheduled successfully!")
        print("⏰ Schedule:")
        print("   • Market Open: 9:15 AM (Mon-Fri)")
        print("   • Daily Signals: 3:00 PM (Mon-Fri)")
        print("   • Market Close: 3:30 PM (Mon-Fri)")
        print("   • Weekend Analysis: 10:00 AM (Saturday)")
    
    def run_scheduler(self):
        """Run the scheduler"""
        self.is_running = True
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print("\n🛑 Scheduler stopped by user")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                time.sleep(60)
    
    def start_scheduler(self):
        """Start scheduler in a separate thread"""
        if self.scheduler_thread is None or not self.scheduler_thread.is_alive():
            self.schedule_jobs()
            self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print(f"🚀 Scheduler started at {datetime.now(self.ist)}")
            return True
        else:
            print("⚠️  Scheduler is already running")
            return False
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        print(f"🛑 Scheduler stopped at {datetime.now(self.ist)}")
    
    def get_next_jobs(self):
        """Get information about next scheduled jobs"""
        jobs_info = []
        for job in schedule.jobs:
            next_run = job.next_run
            if next_run:
                jobs_info.append({
                    'job': str(job),
                    'next_run': next_run.strftime('%Y-%m-%d %H:%M:%S'),
                    'function': job.job_func.__name__
                })
        return sorted(jobs_info, key=lambda x: x['next_run'])
    
    def send_scheduler_status(self):
        """Send scheduler status to Telegram"""
        next_jobs = self.get_next_jobs()
        
        message = f"""⏰ <b>SCHEDULER STATUS</b>
📅 {datetime.now(self.ist).strftime('%A, %B %d, %Y - %H:%M IST')}

🟢 <b>Status:</b> {'Running' if self.is_running else 'Stopped'}

📋 <b>Next Jobs:</b>"""
        
        for job in next_jobs[:5]:  # Show next 5 jobs
            message += f"\n• {job['function']}: {job['next_run']}"
        
        message += f"\n\n🏪 <b>Market Status:</b> {'Open' if self.is_market_day() else 'Closed'}"
        
        self.bot.send_message(message)

def main():
    """Main function to run the scheduler"""
    scheduler = DailyScheduler()
    
    # Send startup message
    startup_message = f"""🚀 <b>SCHEDULER STARTED</b>
📅 {datetime.now(scheduler.ist).strftime('%A, %B %d, %Y - %H:%M IST')}

⏰ <b>Automated Schedule:</b>
• 9:15 AM: Market Open Alert
• 3:00 PM: Daily Signals
• 3:30 PM: Market Close
• 10:00 AM (Sat): Weekend Analysis

🤖 Bot is now monitoring markets automatically!

Type /help for manual commands."""
    
    scheduler.bot.send_message(startup_message)
    
    try:
        # Start scheduler
        scheduler.start_scheduler()
        
        # Keep the main thread alive
        while True:
            time.sleep(3600)  # Sleep for 1 hour
            
            # Optional: Send daily heartbeat
            if datetime.now(scheduler.ist).minute == 0:  # Every hour
                print(f"💓 Scheduler heartbeat: {datetime.now(scheduler.ist)}")
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop_scheduler()
        
        # Send shutdown message
        shutdown_message = f"""🛑 <b>SCHEDULER STOPPED</b>
📅 {datetime.now(scheduler.ist).strftime('%A, %B %d, %Y - %H:%M IST')}

❌ Automated messages are now disabled
💡 Restart the scheduler to resume auto-updates

Manual commands still work:
• /getsignals - Get live signals
• /help - Show all commands"""
        
        scheduler.bot.send_message(shutdown_message)

if __name__ == "__main__":
    main()