from logs.logging import logger
import os
from typing import Final

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
)

from .utils import transcribe_voice_message
from .chat_gpt import greet_user, respond_to_user

# Load environment variables from the specified path
load_dotenv()


class TelegramBot:
    def __init__(self):
        self.TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
        self.BOT_USERNAME: Final = os.getenv("BOT_NAME")
        self.user_choice = None  # Initialize user_choice as None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # keyboard = InlineKeyboardMarkup.from_button(
            #     InlineKeyboardButton("Click to start", callback_data="start_lesson_button")
            # )

            # TODO: remove the keyboard after the user will choose his preferred mode
            user = update.message.from_user
            reply_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton("Text"), KeyboardButton("Voice")],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
            await update.message.reply_text(
                f"Hi {user.first_name}! How would you like to communicate with me?",
                reply_markup=reply_markup,
            )

            await update.message.reply_text(
                greet_user(update.effective_user.first_name),
                # f"Hello {update.effective_user.first_name}, Welcome to teacherBot which will teach you to write, read and speak in English.",
                # reply_markup=keyboard,
            )

        except Exception as e:
            logger.error(f"Error in start_command: {str(e)}")

    # Define a function to handle the user's choice
    async def handle_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_choice = update.message.text
            self.user_choice = (
                user_choice  # Store the user's choice in the class variable
            )

            if user_choice == "Text":
                await update.message.reply_text("Great! You chose text messages.")
            elif user_choice == "Voice":
                await update.message.reply_text("Excellent! You chose voice messages.")
            else:
                await update.message.reply_text(
                    "I'm not sure what you mean. Please choose 'Text' or 'Voice' from the provided options."
                )
        except Exception as e:
            logger.error(f"Error in handle_message: {str(e)}")

    # Define a callback query handler for the button
    async def lesson_button_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        try:
            await update.callback_query.message.reply_text("How are you? ")
        except Exception as e:
            logger.error(f"Error in lesson_button_callback: {str(e)}")

    def handle_response(self, text: str) -> str:
        try:
            response = respond_to_user(text)
            return response

        except Exception as e:
            logger.error(f"Error in handle_response: {str(e)}")
            print(f"Error in handle_response: {str(e)}")

    async def handle_audio(self, update: Update, context: ContextTypes):
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

                transcription = transcribe_voice_message(audio_file_id)

                response: str = self.handle_response(transcription)

                print("Bot: ", response)
                await update.message.reply_text(response)

        except Exception as e:
            logger.error(f"Error in handle_audio: {str(e)}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            text: str = update.message.text
            user_name = update.effective_user.first_name
            logger.info(f"User [{user_name}]: {text}")
            print(f"User [{user_name}]:", text)
            if self.user_choice == "Text":
                logger.info("Text Mode")
                response: str = self.handle_response(text)
            elif self.user_choice == "Voice":
                logger.info("Voice Mode")
                # TODO: have to replace the handle_response function with a new function that will handle the voice mode
                response: str = self.handle_response(text)
            else:
                logger.warning("User has not made a choice yet")
                # Handle the case when the user hasn't made a choice yet
                response = "Please choose 'Text' or 'Voice' first."

            print("Bot:", response)
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error in handle_message: {str(e)}")

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            logger.error(f"Update {update} caused error {context.error}")
        except Exception as e:
            logger.error(f"Error in error handler: {str(e)}")

    def run_bot(self):
        logger.info("Starting bot...")
        print("Starting bot...")
        app = ApplicationBuilder().token(self.TOKEN).build()

        # Commands
        app.add_handler(CommandHandler("start", self.start_command))

        app.add_handler(
            MessageHandler(
                filters.TEXT & filters.Regex(r"(Text|Voice)"), self.handle_choice
            )
        )

        # # Messages
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        app.add_handler(MessageHandler(filters.VOICE, self.handle_audio))
        # Register the callback query handler
        app.add_handler(
            CallbackQueryHandler(
                self.lesson_button_callback, pattern="start_lesson_button"
            )
        )

        # Errors
        app.add_error_handler(self.error)

        app.run_polling(poll_interval=3)
