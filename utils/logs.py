import logging

# Configure logging to print logs to console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the root logger
root_logger = logging.getLogger()

# Set the level of the root logger to DEBUG
root_logger.setLevel(logging.INFO)

# Define a logger
logger = logging.getLogger(__name__)