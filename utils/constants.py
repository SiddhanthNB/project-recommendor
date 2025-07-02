import os
import yaml
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

APP_ENV = os.getenv('APP_ENV', 'production')

SUPABASE_DB_PASSWORD = os.getenv('SUPABASE_DB_PASSWORD')
SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL').replace('[YOUR-PASSWORD]', quote_plus(SUPABASE_DB_PASSWORD))

ATLAS_DB_PASSWORD = os.getenv('ATLAS_DB_PASSWORD')
ATLAS_DB_URL = os.getenv('ATLAS_DB_URL').replace('<db_password>', quote_plus(ATLAS_DB_PASSWORD))

ATLAS_DB_NAME = os.getenv('ATLAS_DB_NAME')
RECOMMENDATION_COLLECTION_NAME = os.getenv('RECOMMENDATION_COLLECTION_NAME')

try:
    with open('utils/services.yaml', 'r') as f:
        _config_str = f.read()
    _config_str = _config_str.format(**os.environ)
    _settings = yaml.safe_load(_config_str)
except FileNotFoundError:
    raise Exception(f"Config file not found!")
except KeyError as e:
    raise Exception(f"Missing environment variable: {e}")
except Exception as e:
    raise Exception(f"Error reading config file: {e}")

API = _settings['api']
