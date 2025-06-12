from database.database_connection_mysql import get_connection
from model.image import Image

CREATE_TABLE_TEXT = """
    CREATE TABLE IF NOT EXISTS images (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        url TEXT NOT NULL
    );
    """

INSERT_IMAGE = "INSERT INTO images (file_name, created_date, url) VALUES (%s, %s, %s)"
SELECT_IMAGES = "SELECT * FROM images LIMIT %s OFFSET %s"
SELECT_TOTAL_IMAGES = "SELECT COUNT(*) AS total FROM images"
SELECT_IMAGE = "SELECT id, file_name, created_date, url FROM images WHERE id = %s"
UPDATE_IMAGE = "UPDATE images SET file_name = %s, created_date = %s, url = %s WHERE id = %s"
DELETE_IMAGE = "DELETE FROM images WHERE id = %s"


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = CREATE_TABLE_TEXT
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'images' created or already exists.")


def insert_image(item: Image):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        INSERT_IMAGE,
        (item.file_name, item.created_date, item.url)
    )
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    conn.close()
    return item


def get_images(limit: int = 20, offset: int = 0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get items with LIMIT and OFFSET
    cursor.execute(SELECT_IMAGES, (limit, offset))
    items = cursor.fetchall()

    # Optional: get total count
    cursor.execute(SELECT_TOTAL_IMAGES)
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return {
        "limit": limit,
        "offset": offset,
        "total": total,
        "data": items
    }


def get_image(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(SELECT_IMAGE, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not item:
        return None
    return Image(**item)



def update_image(item_id: int, item: Image):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        UPDATE_IMAGE,
        (item.file_name, item.created_date, item.url, item_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount  # <--- Check how many rows were updated
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    item.id = item_id
    return item


def delete_image(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(DELETE_IMAGE, (item_id,))
    conn.commit()
    rows_affected = cursor.rowcount  # Check if any row was deleted
    cursor.close()
    conn.close()
    if rows_affected == 0:
        return False
    return True
