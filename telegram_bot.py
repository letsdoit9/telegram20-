import os
import requests
import json
from datetime import datetime
import time
import threading
from streamlit_app import run_screener_logic, format_telegram_message

# Configuration
TELEGRAM_BOT_TOKEN = "7923075723:AAGL5-DGPSU0TLb68vOLretVwioC6vK0fJk"
TELEGRAM_CHAT_ID = "457632002"
ACCESS_TOKEN = os.getenv('UPSTOX_ACCESS_TOKEN', '')  # Set this in environment variables

class TelegramBot:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.access_token = ACCESS_TOKEN
        self.last_update_id = 0
        
    def send_message(self, message, parse_mode='HTML'):
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=payload, timeout=30)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def get_updates(self):
        """Get updates from Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {'offset': self.last_update_id + 1, 'timeout': 30}
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data['ok'] and data['result']:
                    return data['result']
            return []
        except Exception as e:
            print(f"Error getting updates: {e}")
            return []
    
    def handle_swingtop5_command(self):
        """Handle /swingtop5 command"""
        message = """🎯 <b>SWING TRADE FILTER CRITERIA</b>

📋 <b>Filters Applied:</b>

1️⃣ ✅ <b>Risk/Reward Ratio ≥ 2</b> (Strict. Exception only for bluechips with sector momentum.)
2️⃣ ✅ <b>CMP between ₹50 and ₹2000</b>
3️⃣ ✅ <b>Volume ≥ 1.5x 30D Avg</b> OR visible strong breakout momentum
4️⃣ ✅ <b>RSI(14) between 40 and 65</b>
5️⃣ ✅ <b>Prefer trending sectors:</b>
Finance🔥 | Infra | Power🔥 | PSU🔥 | AMC | IT🔥 | Renewable | Pharma | Defence🔥 | FMCG

🎖 <b>Priority Order:</b>
Bluechip > Largecap > Midcap
🔥 Prefer stocks with sector tailwind

📊 <b>Output Format:</b>
🔢 Stock | Entry | SL | Target | R/R | RSI | Sector | Comment 🌟

🟢 <b>Special Notes:</b>
• 🔥 indicates trending sectors
• Borderline R/R accepted for high-conviction bluechips
• Focus on technical breakouts with volume confirmation

💡 <b>Use /getsignals to get live swing trade picks!</b>"""
        
        return self.send_message(message)
    
    def handle_backtest_command(self):
        """Handle /backtest command"""
        message = """📈 <b>BACKTESTING GUIDE</b>

🔍 <b>How to Backtest Your Strategy:</b>

<b>Step 1: Data Collection</b>
• Use historical data (minimum 1 year)
• Include OHLCV data for all stocks
• Ensure data quality and accuracy

<b>Step 2: Strategy Rules</b>
• Define entry conditions clearly
• Set stop loss and target rules
• Include position sizing rules

<b>Step 3: Execution</b>
• Run strategy on historical data
• Record all trades (entry, exit, P&L)
• Include transaction costs (0.1-0.2%)

<b>Step 4: Analysis Metrics</b>
• Win Rate: % of profitable trades
• Average R/R: Avg profit / Avg loss
• Maximum Drawdown: Largest loss streak
• Sharpe Ratio: Risk-adjusted returns
• Total Return vs Buy & Hold

<b>Step 5: Validation</b>
• Test on multiple time periods
• Out-of-sample testing
• Walk-forward analysis

⚠️ <b>Important Notes:</b>
• Past performance ≠ Future results
• Include slippage and real market conditions
• Test during different market cycles
• Paper trade before live implementation

💡 <b>Tools:</b> Python (pandas, numpy), Excel, TradingView, Zerodha Streak"""
        
        return self.send_message(message)
    
    def handle_getsignals_command(self):
        """Handle /getsignals command"""
        if not self.access_token:
            return self.send_message("❌ Access token not configured. Please set UPSTOX_ACCESS_TOKEN environment variable.")
        
        self.send_message("🔄 <b>Scanning markets for signals...</b>\nThis may take 30-60 seconds...")
        
        try:
            # Run swing trade screening
            results = run_screener_logic(self.access_token, scan_limit=200, swing_mode=True)
            
            if results:
                message = format_telegram_message(results, swing_mode=True)
                
                # Add sector summary
                sector_count = {}
                for stock in results[:10]:
                    sector = stock['sector']
                    sector_count[sector] = sector_count.get(sector, 0) + 1
                
                if sector_count:
                    message += "\n🏷 <b>Sector Summary:</b>\n"
                    for sector, count in sorted(sector_count.items(), key=lambda x: x[1], reverse=True):
                        message += f"• {sector}: {count} stocks\n"
                
                message += f"\n⏰ Updated: {datetime.now().strftime('%H:%M:%S')}"
                
                return self.send_message(message)
            else:
                return self.send_message("❌ No qualifying swing trade setups found. Market conditions may not be favorable.")
                
        except Exception as e:
            return self.send_message(f"❌ Error generating signals: {str(e)}")
    
    def handle_help_command(self):
        """Handle /help command"""
        message = """🤖 <b>STOCK SCREENER BOT - COMMANDS</b>

📋 <b>Available Commands:</b>

🎯 <b>/swingtop5</b>
• Shows swing trade filter criteria
• Explains R/R ratio, volume, RSI filters
• Lists trending sectors

📊 <b>/getsignals</b>
• Runs live market scan
• Returns top 5 swing trade picks
• Includes entry, target, stop loss
• Shows R/R ratio and sector info

📈 <b>/backtest</b>
• Complete backtesting guide
• Step-by-step process
• Key metrics to track
• Validation techniques

❓ <b>/help</b>
• Shows this command list

⚙️ <b>Features:</b>
• Real-time market data
• 20+ technical indicators
• Sector-wise analysis
• Risk management focus

🔔 <b>Auto Updates:</b>
• Daily signals at 3:00 PM
• Market hours monitoring
• Breaking news alerts

💡 <b>Pro Tip:</b> Use /getsignals for fresh market opportunities!

🚀 <b>Happy Trading!</b> 📈"""
        
        return self.send_message(message)
    
    def handle_unknown_command(self, command):
        """Handle unknown commands"""
        message = f"""❓ <b>Unknown Command: {command}</b>

Available commands:
• /swingtop5 - Swing trade criteria
• /getsignals - Live market signals  
• /backtest - Backtesting guide
• /help - Show all commands

💡 Type /help for detailed information."""
        
        return self.send_message(message)
    
    def process_message(self, message):
        """Process incoming message"""
        try:
            text = message.get('text', '').strip().lower()
            
            if text.startswith('/'):
                command = text.split()[0]
                
                if command == '/swingtop5':
                    return self.handle_swingtop5_command()
                elif command == '/backtest':
                    return self.handle_backtest_command()
                elif command == '/getsignals':
                    return self.handle_getsignals_command()
                elif command == '/help' or command == '/start':
                    return self.handle_help_command()
                else:
                    return self.handle_unknown_command(command)
            else:
                # Non-command message
                return self.send_message("🤖 Hi! I'm your Stock Screener Bot.\n\nType /help to see available commands.")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            return self.send_message("❌ Error processing your request. Please try again.")
    
    def run_bot(self):
        """Main bot loop"""
        print(f"🤖 Telegram Bot started at {datetime.now()}")
        print(f"📱 Monitoring chat ID: {self.chat_id}")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update['update_id']
                    
                    if 'message' in update:
                        message = update['message']
                        
                        # Check if message is from authorized chat
                        chat_id = str(message['chat']['id'])
                        if chat_id == self.chat_id:
                            print(f"📨 Received: {message.get('text', 'Non-text message')}")
                            self.process_message(message)
                        else:
                            print(f"❌ Unauthorized chat ID: {chat_id}")
                
                time.sleep(1)  # Small delay to prevent API rate limiting
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Bot error: {e}")
                time.sleep(5)  # Wait before retrying
    
    def send_daily_signals(self):
        """Send daily signals - called by scheduler"""
        if not self.access_token:
            return self.send_message("❌ Daily signals failed: Access token not configured.")
        
        try:
            self.send_message("🌅 <b>DAILY MARKET SIGNALS</b>\n🔄 Scanning Nifty 500...")
            
            # Run both screening modes
            swing_results = run_screener_logic(self.access_token, scan_limit=500, swing_mode=True)
            regular_results = run_screener_logic(self.access_token, scan_limit=200, swing_mode=False)
            
            # Send swing trade signals
            if swing_results:
                swing_message = format_telegram_message(swing_results, swing_mode=True)
                swing_message = "🎯 <b>DAILY SWING PICKS</b>\n" + swing_message
                self.send_message(swing_message)
            
            # Send regular screening results
            if regular_results:
                regular_message = format_telegram_message(regular_results, swing_mode=False)
                regular_message = "🚀 <b>DAILY TOP PERFORMERS</b>\n" + regular_message
                self.send_message(regular_message)
            
            if not swing_results and not regular_results:
                self.send_message("📊 Daily Scan Complete\n❌ No qualifying setups found today.\n💡 Market may be consolidating.")
                
        except Exception as e:
            self.send_message(f"❌ Daily signals error: {str(e)}")

def main():
    """Main function to run the bot"""
    bot = TelegramBot()
    
    # Check if access token is configured
    if not bot.access_token:
        print("⚠️  Warning: UPSTOX_ACCESS_TOKEN not set. /getsignals and daily signals will not work.")
        print("💡 Set environment variable: export UPSTOX_ACCESS_TOKEN='your_token_here'")
    
    # Start the bot
    bot.run_bot()

if __name__ == "__main__":
    main()