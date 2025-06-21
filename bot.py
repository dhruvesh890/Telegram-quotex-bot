from telegram.ext import Updater, CommandHandler
import requests
import pandas as pd

API_KEY = "7e20d4d7afde48dda95594e4cc112cb0"
BOT_TOKEN = "7900927113:AAE7NgOnGpznkIvaJUCQSKZeH5J_ozE8uVM"

def analyse(update, context):
    if not context.args:
        update.message.reply_text("❌ Please provide a symbol (e.g., /analyse eur/usd)")
        return

    symbol = context.args[0].upper()
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=30&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        df = pd.DataFrame(data['values'])
        df["close"] = df["close"].astype(float)
        last_price = df["close"].iloc[-1]
        update.message.reply_text(f"📊 {symbol} Price: {last_price}")
    except:
        update.message.reply_text("⚠️ Error fetching data. Symbol invalid or API limit reached.")

def start(update, context):
    update.message.reply_text("✅ Bot is online! Use /analyse eur/usd")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("analyse", analyse))

updater.start_polling()
updater.idle()
