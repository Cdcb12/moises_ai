from decouple import config
from flask import jsonify
import traceback


# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User
# Models
from src.services.AdminService import newUser,newDel,listUsers
from src.services.ChatService import SendMessage

suffix = config('SUFFIX_ADMIN')

class AdminCommands:
    def __init__(self,client: User, command: str):
        try:
            if command.startswith(suffix + "add"):
                parts = command.split()
                if len(parts) == 3:
                    name = parts[1].replace("_", " ")
                    number = parts[2]
                    
                    result = newUser.index(User(number=number,name=name))
                    if result is not None:
                        SendMessage.send(client.number, f"Added {name} with number {number}")


            elif command.startswith(suffix + "del"):
                parts = command.split()
                if len(parts) == 2:
                    number = parts[1]

                    result = newDel.index(User(number=number))
                    if result is None:
                        SendMessage.send(client.number, f"Deleted number {number}")


            elif command.startswith(suffix + "users"):
                result = listUsers()
                if result.index():
                    SendMessage.send(client.number, result.get_list())


        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
