from database.database_connection_mysql import get_connection
from model.item import Item

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT
    );
    """

INSERT_ITEM = "INSERT INTO items (name, description) VALUES (%s, %s)"
SELECT_ITEMS = "SELECT * FROM items LIMIT %s OFFSET %s"
SELECT_TOTAL_ITEMS = "SELECT COUNT(*) AS total FROM items"
SELECT_ITEM = "SELECT id, name, description FROM items WHERE id = %s"
UPDATE_ITEM = "UPDATE items SET name = %s, description = %s WHERE id = %s"
DELETE_ITEM = "DELETE FROM items WHERE id = %s"


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = CREATE_TABLE_TEXT
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'items' created or already exists.")


def insert_item(item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        INSERT_ITEM,
        (item.name, item.description)
    )
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    conn.close()
    return item


def get_items(limit: int = 20, offset: int = 0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get items with LIMIT and OFFSET
    cursor.execute(SELECT_ITEMS, (limit, offset))
    items = cursor.fetchall()

    # Optional: get total count
    cursor.execute(SELECT_TOTAL_ITEMS)
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return {
        "limit": limit,
        "offset": offset,
        "total": total,
        "data": items
    }


def get_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(SELECT_ITEM, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not item:
        return None
    return item


def update_item(item_id: int, item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        UPDATE_ITEM,
        (item.name, item.description, item_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount  # <--- Check how many rows were updated
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    item.id = item_id
    return item


def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(DELETE_ITEM, (item_id,))
    conn.commit()
    rows_affected = cursor.rowcount  # Check if any row was deleted
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    return True
