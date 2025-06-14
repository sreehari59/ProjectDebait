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
                Please first provide a brief opening statement.
                Be assertive. Keep responses concise - 1 sentences maximum."""
            )

            self.side_b = ConversableAgent(
                name="side_b",
                system_message=f"""You are debating in favor of the second option in: {self.topic}.
                Please first provide a brief opening statement.
                Be assertive. Keep responses concise - 1 sentences maximum."""
            )

            self.judge = ConversableAgent(
                name="judge",
                system_message=f"""You are an impartial judge for the debate on: {self.topic}.
                After reviewing the debate transcript, provide a clear verdict declaring the winner.
                Explain your decision in 2-3 sentences based on the strength of arguments, logic, and persuasiveness.
                Format your response as:
                WINNER: [side_a/side_b]
                REASONING: [your explanation]"""
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

        # Generate the judge's verdict
        verdict = self.judge.generate_reply(
            messages=[{
                "role": "user",
                "content": f"Based on the following debate transcript, provide your verdict:\n\n{debate_summary}"
            }]
        )

        print("\nJUDGE'S VERDICT:")
        print(verdict['content'])

if __name__ == "__main__":
    # Example usage
    debate = DebateSystem("cats vs dogs")
    debate.run_debate(rounds=2)
