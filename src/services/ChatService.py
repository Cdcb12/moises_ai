import traceback
import http.client
import json
from decouple import config

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Model
from src.models.PromptModel import Prompt
from src.models.UserModel import User
# Model AI
from src.ai_llms.ClaudeAI import ClaudeCore

class SavePrompt:
    def push_prompt(prompt: Prompt):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO `prompts`(`id`, `id_user`, `prompt`, `predict`, `created_at`) VALUES (NULL, %s, %s, %s, NOW())", (prompt.id, prompt.prompt, prompt.predict))
            
            connection.commit()
            connection.close()
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
        
class SendMessage:
    def send(receive, msg):
        try:
            conn = http.client.HTTPSConnection(config("INFO_BIP_URL_BASE"))
            payload = json.dumps({
                "from": config("TLF_WHATSAPP_BUSSINESS"),  # Your Infobip number
                "to": receive,
                "content": {
                    "text": msg
                }
            })

            headers = {
                'Authorization': 'App '+config("INFO_BIP_API_KEY"),
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            conn.request("POST", "/whatsapp/1/message/text", payload, headers)
            res = conn.getresponse()
            data = res.read()

            return data

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

class PreditionMessage:
    def __init__(self,mx_tokens=None,client:User=None):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT type, model_lenght FROM options WHERE 1")
                row = cursor.fetchone()

                self.model = row[0]
                self.mx_tokens = mx_tokens if mx_tokens is not None else row[1]
                self.client = client

            connection.close()
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    def new(self, prompt):
        try:
            precdition = Prompt(self.client.id, prompt, self.choose_model_precdition(prompt))
            SavePrompt.push_prompt(precdition)
            return SendMessage.send(self.client.number,precdition.predict)

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    def choose_model_precdition(self, prompt):
        try:
            if self.model == "claude":
                return ClaudeCore(self.client, mx_tk=self.mx_tokens).precdition(prompt)

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

