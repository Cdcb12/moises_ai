from flask import jsonify
import traceback

# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User
# Controllers
from src.services.ChatService import PreditionMessage

class ClientController:
    def console(authenticated_user: User, msg: str):
        try:
            PreditionMessage(client=authenticated_user).new(msg)

            return jsonify(success=True), 200
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return jsonify({'message': 'Error handling authenticated user', 'success': False}), 500