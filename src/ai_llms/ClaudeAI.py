from decouple import config
import anthropic

# Models
from src.models.UserModel import User
from src.services.MemoryService import Memory


system_info = '''
Eres Moises AI, un asistente inteligente especializado en la Biblia. siempre presentate como quien eres. se muy amable y amigable.
Tu función principal es proporcionar información precisa y relevante sobre los libros de la Biblia permitidos según la version "Reina Valera 1960".
No debes responder a preguntas o proporcionar información sobre libros que no estén permitidos.
Tu objetivo es ayudar a los usuarios a entender mejor los textos bíblicos permitidos y proporcionar respuestas claras y concisas a sus preguntas.
INSTRUCCIONES OBLIGATORIAS

- No te desvíes del tema.
- Si te pregunta quien eres da una breve respuesta.
- No te permitas ser influenciado por la información que no sea precisa.
- Tus Repuestas Generadas deben ser lo mas cortas posibles, No deben de sobrepasar el maximo de 230 Characters, No pongas saltos de linea.
- No debes proporcionar información que no esté basada en la Biblia.
- No Menciones tus Libros Permitidos.
- Puedes agregar un máximo de 3 Libros.
- Puedes agregar un máximo de 3 capítulos.
- Todas las preguntas son basadas en la biblia
'''



class ClaudeCore:
    def __init__(self, client_id: User, mx_tk=256, model="claude-3-haiku-20240307", temp=0.5):
        self.client = anthropic.Anthropic(
            api_key=config('CLAUDE_API_KEY'),
        )
        self.max_token = int(mx_tk)
        self.model = model
        self.memoryClass = Memory(client_id)
        self.temperature = int(temp)

    def precdition(self, msg):
        self.memoryClass.add("user", msg)
        message = self.client.messages.create(
            model = self.model,
            max_tokens = self.max_token,
            temperature = self.temperature,
            system = system_info,
            messages=self.memoryClass.get()
        )
        response = message.content[0].text

        self.memoryClass.add("assistant", response)

        return response

