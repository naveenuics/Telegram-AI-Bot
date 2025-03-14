import os
import logging
import openai
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(_name_)

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("7572276136:AAFenj87nxMdTKrjuyEWTT7IXwvagUHpZPQ")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

# Function to handle text messages
async def handle_text(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply_text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong.")

# Function to generate an image
async def generate_image(update: Update, context: CallbackContext):
    try:
        user_prompt = " ".join(context.args)
        response = openai.Image.create(prompt=user_prompt, n=1, size="512x512")
        image_url = response["data"][0]["url"]
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Failed to generate image.")

# Start function
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    app.add_handler(CommandHandler("image", generate_image))

    app.run_polling()

if _name_ == "_main_":
    main()
