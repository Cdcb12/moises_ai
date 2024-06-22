from decouple import config
from flask import jsonify
import traceback

# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User
# Controllers
from src.controllers.CommandsController import AdminCommands
from src.services.ChatService import PreditionMessage
from src.services.ChatService import SendMessage

adminActive = False
suffix = config('SUFFIX_ADMIN')

class AdminController:
    def console(authenticated_user: User, msg: str):
        global adminActive  # Add this line
        try:
            if msg.startswith(suffix + "exit"):
                adminActive = False
            elif msg.startswith(suffix + "admin"):
                SendMessage.send(authenticated_user.number, "Admin Active")
                adminActive = True
            elif not adminActive:
                PreditionMessage(client=authenticated_user).new(msg)
            elif adminActive:
                AdminCommands(authenticated_user, msg)
                
            return jsonify(success=True), 200
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return jsonify({'message': 'Error handling authenticated user', 'success': False}), 500