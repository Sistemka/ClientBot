import os
import logging
from pathlib import Path

import dotenv

from .paths import BASE_DIR

dotenv.load_dotenv(Path(BASE_DIR, 'settings', 'env'))

IS_DEBUG = os.environ.get('DEBUG') == '1'

TG_TOKEN = os.environ['TG_TOKEN']

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if IS_DEBUG else logging.INFO
)

PG_CONN = {
    'host': os.environ.get('PG_HOST', 'localhost'),
    'user': os.environ.get('PG_USER'),
    'database': os.environ.get('PG_DATABASE'),
    'password': os.environ.get('PG_PASSWORD'),
}
