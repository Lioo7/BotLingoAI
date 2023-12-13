from bot.telegram_bot import TelegramBot  # run telegram bot server

# from config.config import DB_CONFIG
# from database.PostgreSQL import PostgreSQL
from logs.logging import logger

logger.info("The app is running...")
print("The app is running...")

# db = PostgreSQL(**DB_CONFIG)
# db.connect()
# db.create_tables()
# db.save_user_to_db('Lior', '0501234567','lior@gmail.com')
# db.disconnect()

bt = TelegramBot()
bt.run_bot()
