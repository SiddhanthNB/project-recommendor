import utils.constants as constants
from config.logger import logger
from mongoengine import connect, DEFAULT_CONNECTION_NAME

logger.info(f"Connecting to MongoDB Atlas...")
_connection = connect(db = constants.ATLAS_DB_NAME, host=constants.ATLAS_DB_URL, alias = DEFAULT_CONNECTION_NAME)
logger.info(f"Connected to MongoDB Atlas with connection alias: {DEFAULT_CONNECTION_NAME}")
