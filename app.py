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

    def __call__(self,message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = self.client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = self.messages
        )
        return completion.choices[0].message.content
    
system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

get_planet_mass:
e.g. get_planet_mass: Earth
Returns the mass of the planet in kg

Example session:

Question: What is the mass of Earth times 2?
Thought: I should look for the mass of Earth
Action: get_planet_mass: Earth
PAUSE

You will be called again with this:

Observation: 5.972e24

Thought: I should multiply this by 2
Action: calculate: 5.972e24 * 2
PAUSE

You will be called again with this:

Observation: 1.1944e25

If you have the answer to the question, output it like this:
Answer: The mass of Earth times 2 is 1.1944e25 kg

Now it's your turn:
""".strip()

# tools
def calculate(expression):
    return eval(expression)

def get_planet_mass(planet):
    planet_masses = {
        "Mercury": 3.3011e23,
        "Venus": 4.8675e24,
        "Earth": 5.972e24,
        "Mars": 6.4171e23,
        "Jupiter": 1.8982e27,
        "Saturn": 5.6834e26,
        "Uranus": 8.6810e25,
        "Neptune": 1.02413e26
    }
    return planet_masses.get(planet, "Unknown planet")

neil_dagrasse = Agent(client, system_prompt)

question = "What is the mass of Earth times 5?"

answer = neil_dagrasse(question)
print(answer)

print(neil_dagrasse.messages)

result = neil_dagrasse()
print(result)

observation = get_planet_mass("Earth")
print(observation)

next_prompt = f"Observation: {observation}"
result = neil_dagrasse(next_prompt)
print(result)

result = neil_dagrasse()
print(result)

observation = calculate("5.972e24 * 5")
print(observation)

next_prompt = f"Observation: {observation}"
result = neil_dagrasse(next_prompt)
print(result)

print(neil_dagrasse.messages)