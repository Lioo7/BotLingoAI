import logging
import os
import sys

# Configure the logger to write log entries to a file in the 'logs' directory
log_file = os.path.join('../logs', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)