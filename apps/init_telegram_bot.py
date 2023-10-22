from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
# from logs.logging import logger
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_NAME')

email, age = range(2)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}, Welcome to teacherBot which will teach you to write, read and speak in English."
    )

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Click to start 📜", callback_data="button_clicked")
    )
    await update.message.reply_text(
        "Please fill in some details:", reply_markup=keyboard
    )

def handle_response(text: str) -> str:
    processed = text

    if "@" and "." in processed:
        global email
        email = processed
        return "Enter your age: "

    if processed.isnumeric():
        if int(processed) > 3 and int(processed) < 99:
            global age
            age = processed
            return "The details have been filled in successfully!"

    if "i love python" in processed:
        return "Remember to subscribe!"

    return "I do not understand what you wrote"


# Define a callback query handler for the button
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Enter your email: ")


# Define a callback query handler for the button
async def lesson_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("How are you? ")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
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


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# logger.info("Starting bot...")

app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start_command))

# Messages
app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Register the callback query handler
app.add_handler(CallbackQueryHandler(button_callback, pattern="button_clicked"))
app.add_handler(
    CallbackQueryHandler(lesson_button_callback, pattern="lesson_button_clicked")
)

# Errors
app.add_error_handler(error)

# Polls the bot
# logger.info("Polling...")

app.run_polling(poll_interval=3)
