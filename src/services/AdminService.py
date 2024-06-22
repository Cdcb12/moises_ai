import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User

class updateActivity:
    def index(user: User):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE tester SET last_actitvity=NOW() WHERE number_phone = %(number_phone)s AND not type='owner'", {'number_phone': user.number})
            connection.commit()
            connection.close()
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

class newUser:
    def index(user: User):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")
                try:
                    cursor.execute("SELECT `id` FROM tester WHERE number_phone = %(number_phone)s", {'number_phone': user.number})
                    row = cursor.fetchone()
                    if row is None:
                        cursor.execute("INSERT INTO tester (`id`, `type`, `name`, `number_phone`, `created_at`, `ban`, `last_actitvity`) VALUES (NULL, 'tester', %(name)s, %(number_phone)s, NOW(), 'FALSE', NULL)", {'name': user.name, 'number_phone': user.number})
                    connection.commit()
                except Exception as ex:
                    connection.rollback()
                    Logger.add_to_log("error", str(ex))
                    Logger.add_to_log("error", traceback.format_exc())
            connection.close()
            return row
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

class newDel:
    def index(user: User):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT `id` FROM tester WHERE number_phone = %(number_phone)s AND not type='owner'", {'number_phone': user.number})
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute("DELETE FROM tester WHERE number_phone = %(number_phone)s", {'number_phone': user.number})
            connection.commit()
            connection.close()
            return row
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

class listUsers:
    def __init__(self) -> None:
        self.row = None

    def get_list(self):
        user_list = []
        for row in self.row:
            user_list.append("{} / {}\n{}".format(row[0], row[2], row[1]))

        return "\n".join(user_list)

    def index(self):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT `id`,`number_phone`,`name` FROM tester WHERE not type='owner'")
                self.row = cursor.fetchall()
            connection.close()
            return self.row
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())