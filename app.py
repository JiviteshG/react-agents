import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY not found in .env")

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