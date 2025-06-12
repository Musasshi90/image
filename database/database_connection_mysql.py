import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# Load from parent directory (project/)
env_path = Path(__file__).resolve().parents[1] / ".env"
print(f'DEBUG env_path : {env_path}')
load_dotenv(dotenv_path=env_path)
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

# Replace with your actual FreeSQLDatabase credentials
db_config = {
    "host": MY_SQL_HOST,
    "user": MY_SQL_USERNAME,
    "password": MY_SQL_PASSWORD,
    "database": MY_SQL_DATABASE,
    "port": MY_SQL_PORT,  # Use if specified by provider
}


def get_connection():
    conn = mysql.connector.connect(**db_config)
    return conn
