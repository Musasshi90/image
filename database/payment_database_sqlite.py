from database.database_connection_mysql import get_connection
from model.payment import Payment
import sqlite3
import constant

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        botToken TEXT NOT NULL,
        accountId TEXT NOT NULL,
        currency TEXT DEFAULT 'AUD',
        amount REAL NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        referenceCode TEXT NOT NULL,
        smsUniqueCode TEXT NOT NULL UNIQUE,
        remitter TEXT NOT NULL
    );
    """

INSERT_PAYMENT = "INSERT INTO payments (botToken, accountId, currency, amount, title, content, referenceCode, smsUniqueCode, remitter) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
SELECT_PAYMENT = "SELECT * FROM payments WHERE accountId = ? AND smsUniqueCode = ?"


def create_table():
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    # 2. Create a table (if it doesn't already exist)
    cursor.execute(CREATE_TABLE_TEXT)
    conn.commit()  # Commit the transaction to save changes
    conn.close()
    print("Table 'items' created or already exists.")


def insert_payment(item: Payment):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(INSERT_PAYMENT,
                   (
                       item.botToken,
                       item.accountId,
                       item.currency,
                       item.amount,
                       item.title,
                       item.content,
                       item.referenceCode,
                       item.smsUniqueCode,
                       item.remitter
                   ))
    conn.commit()  # Commit changes to the database
    conn.close()
    item.id = cursor.lastrowid
    return item


def get_payment(accountId: str, smsUniqueCode: str):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    # Make rows return as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # SQLite uses `?` for placeholders
    cursor.execute(
        SELECT_PAYMENT
        , (accountId, smsUniqueCode)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return None
    # Convert row to dictionary
    return Payment(**dict(row))
