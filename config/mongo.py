import utils.constants as constants
from mongoengine import connect, DEFAULT_CONNECTION_NAME

_connection = connect(db = constants.ATLAS_DB_NAME, host=constants.ATLAS_DB_URL, alias = DEFAULT_CONNECTION_NAME)
