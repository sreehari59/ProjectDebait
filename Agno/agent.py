import os

from agno.agent import Agent, RunResponse
from agno.models.mistral import MistralChat
from dotenv import load_dotenv

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")


agent = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=mistral_api_key,
    ),
    markdown=True
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")
