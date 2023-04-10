import hashlib
import logging
import openai
import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

promt_dict = {0:"test_value"}
personaMessage = "Answer as God almighty"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! I am a bot that interacts with ChatGPT-4. Just send me a message, and I will respond with generated text.')

# Gets the persona of the bot for the user
def getPersona(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    personaMessage = promt_dict.get(user_id,"Answer as God almighty")
    update.message.reply_text('Persona for you is : ' + personaMessage)

# Sets the persona of the bot for the user
def setPersona(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    personaMessage = update.message.text
    personaMessage = personaMessage.replace("/set ", "")
    promt_dict[user_id] = personaMessage
    update.message.reply_text('Persona of for you has been set to : ' + personaMessage)

def chat_gpt4(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    user_id = update.message.from_user.id
    personaMessage = promt_dict.get(user_id,"Answer as God almighty")
    prompt = "Answer as " + f"{personaMessage} : {user_input}"
    response_text = chat_gpt4(prompt)
    update.message.reply_text(response_text)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get", getPersona))
    dp.add_handler(CommandHandler("set", setPersona))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
