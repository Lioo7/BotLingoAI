import logging
import os

# Determine the path to the 'logs' directory from the current file's location
logs_dir = os.path.join(os.path.dirname(__file__), "../logs")
log_file = os.path.join(logs_dir, "app.log")

# Ensure that the 'logs' directory exists, and create it if it doesn't
os.makedirs(logs_dir, exist_ok=True)

# Configure the logger to write log entries to the log file
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)

logger = logging.getLogger(__name__)
