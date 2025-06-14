from autogen import ConversableAgent, LLMConfig

# 2. Define our LLM configuration for Mistral
import os

config_list = [
    {
        "api_type": "mistral",
        "model": "mistral-tiny",
        "api_key": os.getenv("MISTRAL_API_KEY"),
    }
]

llm_config = LLMConfig(config_list=config_list)


# 3. Create our LLM agent
with llm_config:
  # Create an AI agent
  assistant = ConversableAgent(
      name="assistant",
      system_message="You are an assistant that responds concisely.",
  )

  # Create another AI agent
  fact_checker = ConversableAgent(
      name="fact_checker",
      system_message="You are a fact-checking assistant.",
  )

# 4. Start the conversation
assistant.initiate_chat(
    recipient=fact_checker,
    message="What is AG2?",
    max_turns=2
)
