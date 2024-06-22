from flask import Blueprint, request, jsonify
import hashlib
import traceback

# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User
# Services
from src.services.AuthService import AuthService
from src.services.AdminService import updateActivity

# Controllers
from src.controllers.AdminController import AdminController
from src.controllers.ClientController import ClientController

main = Blueprint('webhook_blueprint', __name__)

# Create a set to store message hashes
message_hashes = set()


def create_message_hash(message_id: str, sender_number: str, incoming_message: str) -> str:
    """Create a hash of the message"""
    return hashlib.sha256(f"{message_id}{sender_number}{incoming_message}".encode()).hexdigest()

def is_message_duplicate(message_hash: str) -> bool:
    return message_hash in message_hashes

def authController(data: dict) -> tuple:
    try:
        sender_number = data['results'][0]['sender']
        incoming_message = data['results'][0]['content'][0]['text']
        message_id = data['results'][0]['messageId']

        message_hash = create_message_hash(message_id, sender_number, incoming_message)

        if is_message_duplicate(message_hash):
            return jsonify(success=False), 200

        message_hashes.add(message_hash)

        _user = User(number=sender_number)
        authenticated_user = AuthService.auth_user(_user)

        if (authenticated_user != None):
            if authenticated_user.ban == "TRUE":
                return jsonify(success=False), 200

            if authenticated_user.type == "owner":
                return AdminController.console(authenticated_user, incoming_message)
            else:
                updateActivity.index(authenticated_user)
                return ClientController.console(authenticated_user, incoming_message)
        else:
            return jsonify(success=False), 200
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        return jsonify({'message': "ERROR", 'success': False})
    
@main.route('/webhook', methods=['POST'])
def index():
    data = request.json
    return authController(data)