import os

from agno.agent import Agent, RunResponse
from agno.models.mistral import MistralChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from dotenv import load_dotenv

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Create agent storage
agent_storage = SqliteStorage(
    table_name="agent_sessions",
    db_file="tmp/agent_storage.db"
)

agent1 = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=mistral_api_key,
    ),
    storage=agent_storage,
    enable_session_summaries=True,
    session_id="debate_1",
    agent_id="agent1",
    context="You are a debate agent. Respond in a very concise manner. The shorter the better.",
    add_history_to_messages=True,
    num_history_responses=3,
)

agent2 = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=mistral_api_key,
    ),
    storage=agent_storage,
    enable_session_summaries=True,
    session_id="debate_1",
    agent_id="agent2",
    context="You are a debate agent. Respond in a very concise manner. The shorter the better.",
    add_history_to_messages=True,
    num_history_responses=3,
)

judge = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=mistral_api_key,
    ),
    storage=agent_storage,
    enable_session_summaries=True,
    session_id="debate_1",
    agent_id="judge",
    context="You are a debate judge. Respond in a very concise manner. The shorter the better.",
    add_history_to_messages=True,
    num_history_responses=3,
)

agent1.print_response(f"You are debating 'Cats vs. Dogs'. Provide a single argument why Cats are better.")
agent2.print_response(f"You are debating 'Cats vs. Dogs'. Provide a single argument why Dogs are better.")
judge.print_response(f"What side provided the better argument? Respond with 'Cats' or 'Dogs'.")

