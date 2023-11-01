from logs.logging import logger
import os
from typing import Final

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .utils import transcribe_voice_message

# Specify the path to the .env file in the 'config' directory
dotenv_path = os.path.join("config", ".env")

# Load environment variables from the specified path
load_dotenv(dotenv_path)

TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_NAME")

email, age = range(2)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            f"Hello {update.effective_user.first_name}, Welcome to teacherBot which will teach you to write, read and speak in English."
        )

        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Click to start 📜", callback_data="button_clicked")
        )
        await update.message.reply_text(
            "Please fill in some details:", reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error in start_command: {str(e)}")


def handle_response(text: str) -> str:
    try:
        if "@" and "." in text:
            global email
            email = text
            return "Enter your age: "

        if text.isnumeric():
            if int(text) > 3 and int(text) < 99:
                global age
                age = text
                return "The details have been filled in successfully!"

        if "i love python" in text:
            return "Remember to subscribe!"

        return "I do not understand what you wrote"
    except Exception as e:
        logger.error(f"Error in handle_response: {str(e)}")


# Define a callback query handler for the button
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.callback_query.message.reply_text("Enter your email: ")
    except Exception as e:
        logger.error(f"Error in button_callback: {str(e)}")


# Define a callback query handler for the button
async def lesson_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.callback_query.message.reply_text("How are you? ")
    except Exception as e:
        logger.error(f"Error in lesson_button_callback: {str(e)}")


async def handle_audio(update: Update, context: ContextTypes):
    try:
        # Check if the message contains audio
        if update.message.voice:
            audio_file_id = update.message.voice.file_id

            # Define the directory where you want to save voice messages
            voice_messages_dir = "bot/voice_messages"
            # Check if the directory exists, and if not, create it
            if not os.path.exists(voice_messages_dir):
                os.makedirs(voice_messages_dir)

            # Use the bot's 'getFile' method to get the file path
            file = await context.bot.get_file(audio_file_id)
            file_path = os.path.join(voice_messages_dir, f"{audio_file_id}.ogg")

            # Download the audio to the file
            await file.download_to_drive(file_path)

            transcribe_voice_message(audio_file_id)
    except Exception as e:
        logger.error(f"Error in handle_audio: {str(e)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # message_type: str = update.message.chat.type
        text: str = update.message.text

        # logger.info(f'User ({update.effective_user.first_name}) in {message_type}: "{text}"')

        response: str = handle_response(text)

        # logger.info("Bot: ", response)

        if response == "The details have been filled in successfully!":
            keyboard = InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    "Click to start a lesson", callback_data="lesson_button_clicked"
                )
            )
            await update.message.reply_text(response + "\n", reply_markup=keyboard)
        else:
            await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.error(f"Update {update} caused error {context.error}")
    except Exception as e:
        logger.error(f"Error in error handler: {str(e)}")


logger.info("Starting bot...")

app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start_command))

# Messages
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.VOICE, handle_audio))
# Register the callback query handler
app.add_handler(CallbackQueryHandler(button_callback, pattern="button_clicked"))
app.add_handler(
    CallbackQueryHandler(lesson_button_callback, pattern="lesson_button_clicked")
)

# Errors
app.add_error_handler(error)

app.run_polling(poll_interval=3)
