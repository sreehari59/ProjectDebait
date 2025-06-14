import os
from autogen import ConversableAgent, LLMConfig

class DebateSystem:
    def __init__(self, topic):
        self.topic = topic
        self.config_list = [
            {
                "api_type": "mistral",
                "model": "mistral-tiny",
                "api_key": os.getenv("MISTRAL_API_KEY"),
            }
        ]
        self.llm_config = LLMConfig(config_list=self.config_list)
        self.setup_agents()

    def setup_agents(self):
        with self.llm_config:
            self.side_a = ConversableAgent(
                name="side_a",
                system_message=f"""You are debating in favor of the first option in: {self.topic}.
                Make compelling arguments for your side. Be assertive but respectful.
                Keep responses concise - 2-3 sentences maximum."""
            )

            self.side_b = ConversableAgent(
                name="side_b",
                system_message=f"""You are debating in favor of the second option in: {self.topic}.
                Make compelling arguments for your side. Be assertive but respectful.
                Keep responses concise - 2-3 sentences maximum."""
            )

            self.judge = ConversableAgent(
                name="judge",
                system_message=f"""You are an impartial judge for the debate on: {self.topic}.
                Evaluate arguments from both sides based on logic, evidence, and persuasiveness.
                At the end, decide the winner and explain your reasoning briefly."""
            )

    def run_debate(self, rounds=3):
        # Opening statements
        self.side_a.initiate_chat(
            self.side_b,
            message=f"Let's begin our debate about {self.topic}. Here's my opening statement:",
            max_turns=2
        )

        # Debate rounds
        for _ in range(rounds):
            self.side_a.initiate_chat(
                self.side_b,
                message="Your turn. Present your counter-argument.",
                max_turns=3
            )

        # Closing statements
        self.side_a.initiate_chat(
            self.side_b,
            message="Let's make our closing statements. Here's mine:",
            max_turns=2
        )

        # Collect debate history
        side_a_history = [msg for msg in self.side_a.chat_messages[self.side_b]]
        side_b_history = [msg for msg in self.side_b.chat_messages[self.side_a]]
        debate_history = []
        
        # Merge and sort messages by timestamp
        for msg in side_a_history + side_b_history:
            debate_history.append(f"{msg['role']}: {msg['content']}")
        
        debate_summary = "\n".join(debate_history)

        # Have the judge communicate with side_a to deliver the verdict
        self.judge.initiate_chat(
            self.side_a,
            message=f"Based on the following debate:\n\n{debate_summary}\n\nAs the judge, I will now deliver my verdict. Who won and why?",
            max_turns=2
        )

if __name__ == "__main__":
    # Example usage
    debate = DebateSystem("cats vs dogs")
    debate.run_debate(rounds=2)