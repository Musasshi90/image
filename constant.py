import os
from pathlib import Path
from dotenv import load_dotenv

# Load from parent directory (project/)
load_dotenv()
# Mysql config
MY_SQL_HOST = os.getenv("MY_SQL_HOST")
print(f'DEBUG MY_SQL_HOST : {MY_SQL_HOST}')
MY_SQL_USERNAME = os.getenv("MY_SQL_USERNAME")
print(f'DEBUG MY_SQL_USERNAME : {MY_SQL_USERNAME}')
MY_SQL_PASSWORD = os.getenv("MY_SQL_PASSWORD")
print(f'DEBUG MY_SQL_PASSWORD : {MY_SQL_PASSWORD}')
MY_SQL_DATABASE = os.getenv("MY_SQL_DATABASE")
print(f'DEBUG MY_SQL_DATABASE : {MY_SQL_DATABASE}')
MY_SQL_PORT = int(os.getenv("MY_SQL_PORT", 3306))
print(f'DEBUG MY_SQL_PORT : {MY_SQL_PORT}')

# Sqlite config
SQLITE_DB_NAME = os.getenv("SQLITE_DB_NAME")
print(f'DEBUG SQLITE_DB_NAME : {SQLITE_DB_NAME}')

# Supabase config
SUPER_BASE_URL = os.getenv("SUPER_BASE_URL")
print(f'DEBUG SUPER_BASE_URL : {SUPER_BASE_URL}')
SUPABASE_KEY = os.getenv("SUPER_BASE_API_KEY")
print(f'DEBUG SUPABASE_KEY : {SUPABASE_KEY}')
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "images")
print(f'DEBUG STORAGE_BUCKET : {STORAGE_BUCKET}')

USE_LOCAL_DB = os.getenv("USE_LOCAL_DB") == "True"
print(f'DEBUG USE_LOCAL_DB : {USE_LOCAL_DB}')

UPLOAD_DIR = Path("static/uploads")
if USE_LOCAL_DB:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
