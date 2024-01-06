import asyncio
import os
import random
import shutil
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

from logs.logging import logger

from .chat_gpt import process_text_interaction, process_voice_interaction
from .utils import convert_text_to_audio, transcribe_voice_message, split_review_and_followup

# List of possible initial questions
initial_questions = [
    "What's your favorite English word?",
    "Tell me about your day in English.",
    "Can you describe your favorite place using English?",
    "Share a fun fact in English.",
]

# Load environment variables from the specified path
load_dotenv()


class TelegramBot:
    def __init__(self):
        self.TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
        self.BOT_USERNAME: Final = os.getenv("BOT_NAME")

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            if update.message:
                user = update.message.from_user
                if user:
                    await update.message.reply_text(
                        self.greet_user(user.first_name), parse_mode="HTML"
                    )
                    first_question = await self.ask_first_question(
                        user.first_name
                    )
                    print(f"first_question: {first_question}")
                    await asyncio.sleep(2)  # One-unit = one second of delay
                    await update.message.reply_text(first_question)
        except Exception as e:
            logger.error(f"Error in start_command: {str(e)}")

    def handle_text_response(self, text: str) -> str:
        try:
            response = process_text_interaction(text)
            return response

        except Exception as e:
            logger.error(f"Error in handle_text_response: {str(e)}")
            return "An error occurred"

    def handle_voice_response(self, text: str) -> str:
        try:
            response = process_voice_interaction(text)
            return response

        except Exception as e:
            logger.error(f"Error in handle_voice_response: {str(e)}")
            return "An error occurred"

    async def handle_audio(self, update: Update, context: ContextTypes):
        try:
            # Check if the message exists and contains audio
            if update.message and update.message.voice:
                audio_file_id = update.message.voice.file_id

                # Define the directory where you want to save voice messages
                voice_messages_dir = "bot/voice_messages"
                # Check if the directory exists, and if not, create it
                if not os.path.exists(voice_messages_dir):
                    os.makedirs(voice_messages_dir)

                # Use the bot's 'getFile' method to get the file path
                file = await context.bot.get_file(audio_file_id)
                file_path = os.path.join(
                    voice_messages_dir, f"{audio_file_id}.ogg"
                )

                # Download the audio to the file
                await file.download_to_drive(file_path)

                transcription = transcribe_voice_message(audio_file_id)

                response: str = self.handle_voice_response(transcription)
                review, followup = split_review_and_followup(response)

                convert_text_to_audio(review, "bot_review.mp3")
                convert_text_to_audio(followup, "bot_followup.mp3")

                print("Bot Review: ", review)
                await update.message.reply_audio(
                    "bot/voice_messages/bot_review.mp3"
                )
                print("Bot Followup: ", followup)
                await update.message.reply_audio(
                    "bot/voice_messages/bot_followup.mp3"
                )

                # Remove all files from the 'voice_messages' directory
                shutil.rmtree(voice_messages_dir)
                logger.info("Cleared 'voice_messages' directory")

        except Exception as e:
            logger.error(f"Error in handle_audio: {str(e)}")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("handle_message")
        try:
            if update.message:
                text: str = (
                    update.message.text or ""
                )  # Use empty string if text is None
                if update.effective_user:
                    # user_id = update.effective_user.id
                    user_name = update.effective_user.first_name
                    logger.info(f"User [{user_name}]: {text}")
                    print(f"User [{user_name}]:", text)
                    response: str = self.handle_text_response(text)
                    review, followup = split_review_and_followup(response)
                    print("Bot Review:", review)
                    await update.message.reply_text(review)
                    print("Bot Followup:", followup)
                    await update.message.reply_text(followup)
        except Exception as e:
            logger.error(f"Error in handle_message: {str(e)}")

    def greet_user(self, user_name: str) -> str:
        return (
            f"<b>Welcome to BotLingo, {user_name}!</b>\n\n"
            f"👋 Hey {user_name}! Ready to make English learning fun?\n"
            "🎉 I'll guide you through exercises, correct mistakes, and we'll learn together. Any questions? I'm here!\n"
            "💬 Let's start this language journey together!\n"
        )

    async def ask_first_question(self, user_name: str) -> str:
        print("ask_first_question is running")
        # Randomly select an initial question
        random_question = random.choice(initial_questions)
        introduction = f"Let's start with a question: {random_question}"
        return introduction

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

        # Messages
        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, self.handle_message
            )
        )
        app.add_handler(MessageHandler(filters.VOICE, self.handle_audio))
        # Register the callback query handler
        app.add_handler(
            CallbackQueryHandler(
                self.ask_first_question, pattern="ask_first_question"
            )
        )

        # Errors
        app.add_error_handler(self.error)

        app.run_polling(poll_interval=3)
