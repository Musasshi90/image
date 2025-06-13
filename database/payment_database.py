import constant
import database.payment_database_mysql as payment_database_mysql
import database.payment_database_mysql_for_update as payment_database_mysql_for_update
import database.payment_database_sqlite as payment_database_sqlite
import database.payment_database_sqlite_for_update as payment_database_sqlite_for_update
from model.payment import Payment


def create_table():
    if constant.USE_LOCAL_DB:
        payment_database_sqlite.create_table()
        payment_database_sqlite_for_update.create_table()
    else:
        payment_database_mysql.create_table()
        payment_database_mysql_for_update.create_table()


def insert_payment(item: Payment, is_update: bool):
    if constant.USE_LOCAL_DB:
        if not is_update:
            return payment_database_sqlite.insert_payment(item)
        else:
            return payment_database_sqlite_for_update.insert_payment(item)
    else:
        if not is_update:
            return payment_database_mysql.insert_payment(item)
        else:
            return payment_database_mysql_for_update.insert_payment(item)


def get_payment(accountId: str, smsUniqueCode: str, is_update: bool):
    if constant.USE_LOCAL_DB:
        if not is_update:
            return payment_database_sqlite.get_payment(accountId, smsUniqueCode)
        else:
            return payment_database_sqlite_for_update.get_payment(accountId, smsUniqueCode)
    else:
        if not is_update:
            return payment_database_mysql.get_payment(accountId, smsUniqueCode)
        else:
            return payment_database_mysql_for_update.get_payment(accountId, smsUniqueCode)
