import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

agent1 = Agent(
    name="Debater 1",
    instructions="You are a debate agent. Respond in a very concise manner. The shorter the better.",
    model=LitellmModel(model='mistral/mistral-large-latest', api_key=mistral_api_key),
)

agent2 = Agent(
    name="Debater 2", 
    instructions="You are a debate agent. Respond in a very concise manner. The shorter the better.",
    model=LitellmModel(model='mistral/mistral-large-latest', api_key=mistral_api_key),
)

judge = Agent(
    name="Judge", 
    instructions="You are a debate judge. Respond in a very concise manner. The shorter the better.",
    model=LitellmModel(model='mistral/mistral-large-latest', api_key=mistral_api_key),
)

response1 = Runner.run_sync(agent1, input="You are debating 'Cats vs. Dogs'. Provide a single argument why Cats are better.")
print(f"{agent1.name}: {response1.final_output}")

response2 = Runner.run_sync(agent2, input=response1.to_input_list()+[{"content":"Provide a single argument why Dogs are better.", "role": "user"}])
print(f"{agent2.name}: {response2.final_output}")

response3 = Runner.run_sync(judge, input=response2.to_input_list()+[{"content":"What side provided the better argument? Respond with 'Cats' or 'Dogs'.", "role": "user"}])
print(f"{judge.name}: {response3.final_output}")

print(response3.final_output)
