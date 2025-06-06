import os

# Telegram Bot Token
BOT_TOKEN = ""

# Database Configuration
DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql+psycopg2://man:man@localhost:5432/mydb"
DATABASE_NAME = "mydb"
DATABASE_USER = "man"
DATABASE_PASSWORD = "man"
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432

access_key=""
secret_key=""
endpoint_url="https://storage.yandexcloud.net/",
bucket_name="alekseyhouse"
region_name="ru-central1"


# External API Keys
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY") or "YOUR_WEATHER_API_KEY"
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") or "YOUR_GOOGLE_MAPS_API_KEY"

# Other Settings

LOG_LEVEL = "INFO"  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
