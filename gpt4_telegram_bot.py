import logging
import openai
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! I am a bot that interacts with ChatGPT-4. Just send me a message, and I will respond with generated text.')

def chat_gpt4(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    prompt = f"Reply to this user message: \"{user_input}\""
    response_text = chat_gpt4(prompt)
    update.message.reply_text(response_text)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
