import os
import time
import requests
import ccxt
from flask import Flask
import threading

# Web Server to keep Render instance awake
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Scanner is Live 24/7!", 200

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_ BOT_ TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_ CHAT_ ID')

exchange = ccxt.binance({'enableRateLimit': True})

# 50 Institutional Pairs
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT',
    'DOGE/USDT', 'ADA/USDT', 'AVAX/USDT', 'LINK/USDT', 'SUI/USDT',
    'NEAR/USDT', 'APT/USDT', 'DOT/USDT', 'LTC/USDT', 'BCH/USDT',
    'ATOM/USDT', 'ICP/USDT', 'FTM/USDT', 'SEI/USDT', 'TIA/USDT',
    'STX/USDT', 'INJ/USDT', 'RENDER/USDT', 'FET/USDT', 'WLD/USDT',
    'ARB/USDT', 'OP/USDT', 'UNI/USDT', 'AAVE/USDT', 'LDO/USDT',
    'PENDLE/USDT', 'ENA/USDT', 'ONDO/USDT', 'MKR/USDT', 'CRV/USDT',
    'STRK/USDT', 'JUP/USDT', 'PYTH/USDT', 'DYDX/USDT', 'PEPE/USDT',
    'WIF/USDT', 'SHIB/USDT', 'BONK/USDT', 'ORDI/USDT', 'RUNE/USDT',
    'GALA/USDT', 'SAND/USDT', 'MANA/USDT', 'AXS/USDT', 'IMX/USDT'
]

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

def check_market_structure():
    for symbol in SYMBOLS:
        try:
            candles = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=5)
            if not candles: continue
            
            open_price = candles[-2][1]
            close_price = candles[-2][4]
            move_percentage = abs(close_price - open_price) / open_price
            
            if move_percentage > 0.015:
                msg = f"🟢 *SMC ALERT* 🟢\n\n*Pair:* {symbol}\n*Timeframe:* 15m\n*Setup:* Impulse Move / Potential OB\n\n_Check Bookmap for absorption!_"
                send_telegram_alert(msg)
                
            time.sleep(1)
        except:
            time.sleep(1)

def scanner_loop():
    send_telegram_alert("🟢 *SMC 15m SCANNER IS LIVE*\n\nStatus: Active & Monitoring 50 Pairs\nTarget: 15m Institutional Activity")
    while True:
        try:
            check_market_structure()
            time.sleep(900)
        except:
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=scanner_loop, daemon=True).start()
    run_server()
send_telegram_alert("✅ SMC Scanner is ONLINE")
