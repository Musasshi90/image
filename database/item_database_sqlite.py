import sqlite3

import constant
from model.item import Item

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    );
    """

INSERT_ITEM = "INSERT INTO items (name, description) VALUES (?, ?)"
SELECT_ITEMS = "SELECT * FROM items LIMIT ? OFFSET ?"
SELECT_TOTAL_ITEMS = "SELECT COUNT(*) AS total FROM items"
SELECT_ITEM = "SELECT id, name, description FROM items WHERE id = ?"
UPDATE_ITEM = "UPDATE items SET name = ?, description = ? WHERE id = ?"
DELETE_ITEM = "DELETE FROM items WHERE id = ?"


def create_table():
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    # 2. Create a table (if it doesn't already exist)
    cursor.execute(CREATE_TABLE_TEXT)
    conn.commit()  # Commit the transaction to save changes
    conn.close()
    print("Table 'items' created or already exists.")


def insert_item(item: Item):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(INSERT_ITEM,
                   (item.name, item.description))
    conn.commit()  # Commit changes to the database
    conn.close()
    item.id = cursor.lastrowid
    return item


def get_items(limit: int = 20, offset: int = 0):
    # Connect to SQLite database
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)

    # Make rows behave like dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get items with LIMIT and OFFSET (SQLite uses `?` as placeholders)
    cursor.execute(SELECT_ITEMS, (limit, offset))
    items = [dict(row) for row in cursor.fetchall()]
    temp_items = [Item(**item) for item in items]

    # Optional: get total count
    cursor.execute(SELECT_TOTAL_ITEMS)
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return {
        "limit": limit,
        "offset": offset,
        "total": total,
        "data": temp_items
    }


def get_item(item_id: int):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)

    # Make rows return as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # SQLite uses `?` for placeholders
    cursor.execute(
        SELECT_ITEM,
        (item_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    # Convert row to dictionary
    return Item(**dict(row))


def update_item(item_id: int, item: Item):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        UPDATE_ITEM,
        (item.name, item.description, item_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount  # ✅ works in sqlite3 too
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    item.id = item_id
    return item


def delete_item(item_id: int):
    conn = sqlite3.connect(constant.SQLITE_DB_NAME)
    cursor = conn.cursor()

    # SQLite uses ? instead of %s for parameters
    cursor.execute(DELETE_ITEM, (item_id,))
    conn.commit()

    rows_affected = cursor.rowcount  # ✅ Still valid in sqlite3

    cursor.close()
    conn.close()

    if rows_affected == 0:
        return False
    return True
