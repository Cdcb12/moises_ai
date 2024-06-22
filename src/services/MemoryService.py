from decouple import config

# Models
from src.models.UserModel import User


history_memory = {}

class Memory():
    def __init__(self, client: User) -> None:
        self.client = client

    def add(self, role, msg):
        global history_memory
        if self.client.id not in history_memory:
            history_memory[self.client.id] = []

        history_memory[self.client.id].append({"role": role, "content": msg})

        if len(history_memory[self.client.id]) >= int(config("MEMORY_CACHE")):
            if history_memory[self.client.id][0]["role"] == "user":
                history_memory[self.client.id].pop(0)
            history_memory[self.client.id].pop(0)

    def get(self):
        return history_memory[self.client.id]


    def del_client_of_memory(id):
        global history_memory
        if id in history_memory:
            del history_memory[id]


    