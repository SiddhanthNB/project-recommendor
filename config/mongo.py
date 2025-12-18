from config.logger import logger
import utils.constants as constants
from mongoengine import connect, DEFAULT_CONNECTION_NAME

logger.info(f"Connecting to MongoDB Atlas...")
_connection = connect(
    db=constants.MONGO_DATABASE_NAME,
    host=constants.MONGO_CLUSTER_URI,
    alias=DEFAULT_CONNECTION_NAME
)
logger.info(f"Connected to MongoDB Atlas with connection alias: {DEFAULT_CONNECTION_NAME}")
