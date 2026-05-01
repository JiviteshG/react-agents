import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY not found in .env")

client = Groq(
     api_key=GROQ_API_KEY
)

# chat_completion = client.chat.completions.create(
#     model = "llama3-70b-instruct",
#     messages = [
#         {"role": "user", 
#          "content": "Explain the advantage of fast language models."},
#         {"role": "system", "content": "You are a helpful assistant."},
#     ]
# )

# print(chat_completion.choices[0].message.content)

class Agent:
    def __init__(self, client, system):
        self.client = client
        self.system = system
        self.messages = []

        if self.system is not None:
                self.messages.append({"role": "system", "content": self.system})

    def __call__(self,message):
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = self.client.chat.completions.create(
            model = "llama3-70b-instruct",
            messages = self.messages
        )
        return completion.choices[0].message.content