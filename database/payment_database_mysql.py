from database.database_connection_mysql import get_connection
from model.payment import Payment

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        botToken VARCHAR(50) NOT NULL,
        accountId VARCHAR(50) NOT NULL,
        currency VARCHAR(50) DEFAULT 'AUD',
        amount DOUBLE(10, 2) NOT NULL,
        title VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        referenceCode VARCHAR(50) NOT NULL,
        smsUniqueCode VARCHAR(50) UNIQUE NOT NULL,
        remitter VARCHAR(50) NOT NULL
    );
    """

INSERT_PAYMENT = "INSERT INTO payments (botToken, accountId, currency, amount, title, content, referenceCode, smsUniqueCode, remitter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
SELECT_PAYMENT = "SELECT * FROM payments WHERE accountId = %s AND smsUniqueCode = %s"


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = CREATE_TABLE_TEXT
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'items' created or already exists.")


def insert_payment(item: Payment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        INSERT_PAYMENT,
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
        )
    )
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    conn.close()
    return item


def get_payment(accountId: str, smsUniqueCode: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(SELECT_PAYMENT, (accountId, smsUniqueCode))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not item:
        return None
    return item
