from logs.logging import logger
from config.config import DB_CONFIG
from database.PostgreSQL import PostgreSQL

logger.info("The app is running...")
print("The app is running...")
db = PostgreSQL(**DB_CONFIG)
db.connect()
db.create_tables()
db.save_user_to_db('Lior', '0501234567','lior@gmail.com')
db.disconnect()

from bot import init_telegram_bot  # run telegram bot server