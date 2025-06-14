import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

class LangChainDebateSystem:
    def __init__(self, topic, side_a_point, side_b_point, rounds=3):
        self.topic = topic
        self.side_a_point = side_a_point
        self.side_b_point = side_b_point
        self.rounds = rounds

        # Set up ChatOpenAI with Mistral's OpenAI-compatible endpoint
        self.llm = ChatOpenAI(
            openai_api_base=os.getenv("MISTRAL_OPENAI_API_BASE", "https://api.mistral.ai/v1"),
            openai_api_key=os.getenv("MISTRAL_API_KEY"),
            model="mistral-tiny",
            temperature=0.3,
        )

        # Prompts
        self.side_a_prompt = PromptTemplate(
            input_variables=["history", "topic"],
            template=(
                "You are concisely arguing FOR: {side_a_point}.\n"
                "Debate topic: {topic}\n"
                "Conversation so far:\n{history}\n"
                "Don't use numbered points or lists.\n"
                "Your next point (1-2 sentences, no pleasantries):"
            )
        )
        self.side_b_prompt = PromptTemplate(
            input_variables=["history", "topic"],
            template=(
                "You are concisely arguing FOR: {side_b_point}.\n"
                "Debate topic: {topic}\n"
                "Conversation so far:\n{history}\n"
                "Don't use numbered points or lists.\n"
                "Your next point (1-2 sentences, no pleasantries):"
            )
        )
        self.judge_prompt = PromptTemplate(
            input_variables=["transcript", "topic"],
            template=(
                "You are judging the debate on: {topic}.\n"
                "Debate transcript:\n{transcript}\n"
                "Evaluate arguments solely on clarity, evidence, and logical reasoning.\n"
                "Format response EXACTLY as:\n"
                "WINNER: [side_a/side_b]\n"
                "REASON: [one clear sentence explanation]"
            )
        )

        # Chains with partials for static arguments
        self.side_a_chain = LLMChain(
            llm=self.llm,
            prompt=self.side_a_prompt.partial(side_a_point=self.side_a_point, topic=self.topic)
        )
        self.side_b_chain = LLMChain(
            llm=self.llm,
            prompt=self.side_b_prompt.partial(side_b_point=self.side_b_point, topic=self.topic)
        )
        self.judge_chain = LLMChain(
            llm=self.llm,
            prompt=self.judge_prompt.partial(topic=self.topic)
        )
    def print_reply(self, agent, message):
        print(f"👨‍💻 {agent}:\n {message}\n\n")

    def run_debate(self):
        history = ""
        print(f"\n\n💬 Debate Topic: {self.topic}\n\n")
        # Opening statement by side A
        msg_a = self.side_a_chain.run(history=history, topic=self.topic)
        self.print_reply("side_a", msg_a)
        history += f"side_a: {msg_a}\n"
        msg_b = self.side_b_chain.run(history=history, topic=self.topic)
        self.print_reply("side_b", msg_b)
        history += f"side_b: {msg_b}\n"

        # Debate rounds
        for _ in range(self.rounds):
            msg_a = self.side_a_chain.run(history=history, topic=self.topic)
            self.print_reply("side_a", msg_a)
            history += f"side_a: {msg_a}\n"
            msg_b = self.side_b_chain.run(history=history, topic=self.topic)
            self.print_reply("side_b", msg_b)
            history += f"side_b: {msg_b}\n"

        # Closing statements
        msg_a = self.side_a_chain.run(history=history, topic=self.topic)
        self.print_reply("side_a", msg_a)
        history += f"side_a: {msg_a}\n"
        msg_b = self.side_b_chain.run(history=history, topic=self.topic)
        self.print_reply("side_b", msg_b)
        history += f"side_b: {msg_b}\n"

        # Judge
        verdict = self.judge_chain.run(transcript=history, topic=self.topic)
        print("\nJUDGE'S VERDICT:")
        print(verdict)

if __name__ == "__main__":
    debate = LangChainDebateSystem(
        topic="cats vs dogs",
        side_a_point="cats are better pets",
        side_b_point="dogs are better pets",
        rounds=2
    )
    debate.run_debate()
