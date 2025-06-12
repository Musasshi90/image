import sqlite3
from model.image import Image
import constant

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        url TEXT NOT NULL
    );
    """

INSERT_IMAGE = "INSERT INTO images (file_name, created_date, url) VALUES (?, ?, ?)"
SELECT_IMAGES = "SELECT * FROM images LIMIT ? OFFSET ?"
SELECT_TOTAL_IMAGES = "SELECT COUNT(*) AS total FROM images"
SELECT_IMAGE = "SELECT id, file_name, created_date, url FROM images WHERE id = ?"
UPDATE_IMAGE = "UPDATE images SET file_name = ?, created_date = ?, url = ? WHERE id = ?"
DELETE_IMAGE = "DELETE FROM images WHERE id = ?"


def create_table():
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    # 2. Create a table (if it doesn't already exist)
    cursor.execute(CREATE_TABLE_TEXT)
    conn.commit()  # Commit the transaction to save changes
    conn.close()
    print("Table 'images' created or already exists.")


def insert_image(item: Image):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(INSERT_IMAGE,
                   (item.file_name, item.created_date, item.url))
    conn.commit()  # Commit changes to the database
    conn.close()
    item.id = cursor.lastrowid
    return item


def get_images(limit: int = 20, offset: int = 0):
    # Connect to SQLite database
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)

    # Make rows behave like dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get items with LIMIT and OFFSET (SQLite uses `?` as placeholders)
    cursor.execute(SELECT_IMAGES, (limit, offset))
    items = [dict(row) for row in cursor.fetchall()]
    images = [Image(**img) for img in items]

    # Optional: get total count
    cursor.execute(SELECT_TOTAL_IMAGES)
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return {
        "limit": limit,
        "offset": offset,
        "total": total,
        "data": images
    }


def get_image(item_id: int):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    # Make rows return as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # SQLite uses `?` for placeholders
    cursor.execute(
        SELECT_IMAGE,
        (item_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    # Convert row to dictionary
    return Image(**dict(row))


def update_image(item_id: int, item: Image):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        UPDATE_IMAGE,
        (item.file_name, item.created_date, item.url, item_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount  # ✅ works in sqlite3 too
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    item.id = item_id
    return item


def delete_image(item_id: int):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()

    # SQLite uses ? instead of %s for parameters
    cursor.execute(DELETE_IMAGE, (item_id,))
    conn.commit()

    rows_affected = cursor.rowcount  # ✅ Still valid in sqlite3

    cursor.close()
    conn.close()

    if rows_affected == 0:
        return False
    return True
