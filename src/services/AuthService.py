import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User

class AuthService:
 
    @classmethod
    def auth_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT `id`, `type`, `name`, `ban` FROM tester WHERE number_phone = %s", (user.number,))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = User(int(row[0]), row[1], user.number, row[2], row[3])
            connection.close()
            return authenticated_user
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())