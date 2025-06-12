import constant
import database.item_database_mysql as item_database_mysql
import database.item_database_sqlite as item_database_sqlite
from model.item import Item


def create_table():
    if constant.USE_LOCAL_DB:
        item_database_sqlite.create_table()
    else:
        item_database_mysql.create_table()


def insert_item(item: Item):
    if constant.USE_LOCAL_DB:
        return item_database_sqlite.insert_item(item)
    else:
        return item_database_mysql.insert_item(item)


def get_items(limit: int = 20, offset: int = 0):
    if constant.USE_LOCAL_DB:
        return item_database_sqlite.get_items(limit, offset)
    else:
        return item_database_mysql.get_items(limit, offset)


def get_item(item_id: int):
    if constant.USE_LOCAL_DB:
        return item_database_sqlite.get_item(item_id)
    else:
        return item_database_mysql.get_item(item_id)


def update_item(item_id: int, item: Item):
    if constant.USE_LOCAL_DB:
        return item_database_sqlite.update_item(item_id, item)
    else:
        return item_database_mysql.update_item(item_id, item)


def delete_item(item_id: int):
    if constant.USE_LOCAL_DB:
        return item_database_sqlite.delete_item(item_id)
    else:
        return item_database_mysql.delete_item(item_id)
