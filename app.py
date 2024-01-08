from bot.telegram_bot import TelegramBot  # run telegram bot server
from logs.logging import logger

logger.info("The app is running...")
print("The app is running...")

bt = TelegramBot()
bt.run_bot()
