import constant
import database.image_database_mysql as image_database_mysql
import database.image_database_sqlite as image_database_sqlite
from model.image import Image


def create_table():
    if constant.USE_LOCAL_DB:
        image_database_sqlite.create_table()
    else:
        image_database_mysql.create_table()


def insert_image(item: Image):
    if constant.USE_LOCAL_DB:
        return image_database_sqlite.insert_image(item)
    else:
        return image_database_mysql.insert_image(item)


def get_images(limit: int = 20, offset: int = 0):
    if constant.USE_LOCAL_DB:
        return image_database_sqlite.get_images(limit, offset)
    else:
        return image_database_mysql.get_images(limit, offset)


def get_image(item_id: int):
    if constant.USE_LOCAL_DB:
        return image_database_sqlite.get_image(item_id)
    else:
        return image_database_mysql.get_image(item_id)


def update_image(item_id: int, item: Image):
    if constant.USE_LOCAL_DB:
        return image_database_sqlite.update_image(item_id, item)
    else:
        return image_database_mysql.update_image(item_id, item)


def delete_image(item_id: int):
    if constant.USE_LOCAL_DB:
        return image_database_sqlite.delete_image(item_id)
    else:
        return image_database_mysql.delete_image(item_id)
