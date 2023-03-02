# A useful script to test the message sending and get config data for the Telegram bot
# ref https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2
# bot instructions: https://core.telegram.org/bots#creating-a-new-bot

import configparser
import requests

# Read the settings from telegram section of modmail.ini
config = configparser.ConfigParser()
config.read("modmail.ini")
TOKEN = config.get("telegram", "bot_token")
chat_id = config.get("telegram", "chat_id")

# this is what is sent
message = "hello from your telegram bot"

# for getting information
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# send the contents of message
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

# does the actual send
print(requests.get(url).json())