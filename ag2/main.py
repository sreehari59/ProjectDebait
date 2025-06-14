import os
from autogen import ConversableAgent, LLMConfig

class DebateSystem:
    def __init__(self, topic, side_a_point, side_b_point):
        self.topic = topic
        self.side_a_point = side_a_point
        self.side_b_point = side_b_point
        self.config_list = [
            {
                "api_type": "mistral",
                "model": "mistral-tiny",
                "api_key": os.getenv("MISTRAL_API_KEY"),
                "temperature": 0.3,  # Lower temperature for more focused responses
            }
        ]
        self.llm_config = LLMConfig(config_list=self.config_list)
        self.setup_agents()

    def setup_agents(self):
        with self.llm_config:
            self.side_a = ConversableAgent(
                name="side_a",
                system_message=f"""You are concisely arguing FOR {self.side_a_point}.
                Make one clear, strong point per response. Don't change side, stay strong.
                Use a 1-2 sentences maximum.
                Never use pleasantries or acknowledgments."""
            )

            self.side_b = ConversableAgent(
                name="side_b",
                system_message=f"""You are concisely arguing FOR: {self.side_b_point}.
                Make one clear, strong point per response. Don't change side, stay strong.
                Use a 1-2 sentences maximum.
                Never use pleasantries or acknowledgments."""
            )

            self.judge = ConversableAgent(
                name="judge",
                system_message=f"""You are judging the debate on: {self.topic}.
                Evaluate arguments solely on clarity, evidence, and logical reasoning.
                Format response EXACTLY as:
                WINNER: [side_a/side_b]
                REASON: [one clear sentence explanation]"""
            )

    def run_debate(self, rounds=3):
        # Opening statements
        self.side_a.initiate_chat(
            self.side_b,
            message=f"Opening statement about {self.topic}:",
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
    debate = DebateSystem("bikes vs cars", "bikes are the best for Karlsruhe", "cars are the best for Germany")
    debate.run_debate(rounds=2)
