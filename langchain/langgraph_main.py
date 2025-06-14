import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Dict, Any
from pydantic import BaseModel, Field
from typing import List

# Define the state schema for LangGraph
class DebateState(BaseModel):
    history: List[str] = Field(default_factory=list)
    round: int = 0
    max_rounds: int = 2

# LLM-based agent logic (require passing debate_system instance)
def side_a_node(state: DebateState, debate_system=None) -> DebateState:
    # Use LLM to generate side A's response
    history_str = "\n".join(state.history)
    msg = debate_system.side_a_prompt.format(
        side_a_point=debate_system.side_a_point,
        topic=debate_system.topic,
        history=history_str
    )
    response = debate_system.llm.invoke(msg)
    return DebateState(
        history=state.history + [f"side_a: {response.content.strip()}"],
        round=state.round,
        max_rounds=state.max_rounds,
    )

def side_b_node(state: DebateState, debate_system=None) -> DebateState:
    # Use LLM to generate side B's response
    history_str = "\n".join(state.history)
    msg = debate_system.side_b_prompt.format(
        side_b_point=debate_system.side_b_point,
        topic=debate_system.topic,
        history=history_str
    )
    response = debate_system.llm.invoke(msg)
    return DebateState(
        history=state.history + [f"side_b: {response.content.strip()}"],
        round=state.round,
        max_rounds=state.max_rounds,
    )

def judge_node(state: DebateState, debate_system=None) -> Dict[str, Any]:
    # Use LLM to generate judge's verdict
    transcript = "\n".join(state.history)
    msg = debate_system.judge_prompt.format(
        topic=debate_system.topic,
        transcript=transcript
    )
    response = debate_system.llm.invoke(msg)
    return {"verdict": response.content.strip()}

class LangGraphDebateSystem:
    def __init__(self, topic, side_a_point, side_b_point, rounds=2):
        self.topic = topic
        self.side_a_point = side_a_point
        self.side_b_point = side_b_point
        self.rounds = rounds

        # Set up LLM (Mistral via OpenAI-compatible endpoint)
        self.llm = ChatOpenAI(
            openai_api_base=os.getenv("MISTRAL_OPENAI_API_BASE", "https://api.mistral.ai/v1"),
            openai_api_key=os.getenv("MISTRAL_API_KEY"),
            model="mistral-tiny",
            temperature=0.3,
        )

        # Prompts (not yet used in skeleton)
        self.side_a_prompt = PromptTemplate(
            input_variables=["history", "topic"],
            template="You are concisely arguing FOR: {side_a_point}.\nDebate topic: {topic}\nConversation so far:\n{history}\n Put only one concise and short argument. Your next point:"
        )
        self.side_b_prompt = PromptTemplate(
            input_variables=["history", "topic"],
            template="You are concisely arguing FOR: {side_b_point}.\nDebate topic: {topic}\nConversation so far:\n{history}\n Put only one concise and short argument. Your next point:"
        )
        self.judge_prompt = PromptTemplate(
            input_variables=["transcript", "topic"],
            template="You are judging the debate on: {topic}.\nDebate transcript:\n{transcript}\nFormat response EXACTLY as:\nWINNER: [side_a/side_b]\nREASON: [one clear sentence explanation]"
        )

        # Build LangGraph workflow
        # Wrap node functions to inject self (the debate_system instance)
        def side_a_node_wrapped(state):
            return side_a_node(state, debate_system=self)
        def side_b_node_wrapped(state):
            return side_b_node(state, debate_system=self)
        def judge_node_wrapped(state):
            return judge_node(state, debate_system=self)

        self.graph = StateGraph(state_schema=DebateState)
        self.graph.add_node("side_a", side_a_node_wrapped)
        self.graph.add_node("side_b", side_b_node_wrapped)
        self.graph.add_node("judge", judge_node_wrapped)

        # Edges: alternate between side_a and side_b for N rounds, then judge
        self.graph.add_edge("side_a", "side_b")
        self.graph.add_edge("side_b", "side_a")
        self.graph.add_edge("side_a", "judge")  # After last round, go to judge

        # Set entry and exit points
        self.graph.set_entry_point("side_a")
        self.graph.set_finish_point("judge")

        # Compile the workflow
        self.workflow = self.graph.compile()

    def run_debate(self):
        # Initial state
        state = DebateState(
            history=[f"Debate topic: {self.topic}"],
            round=0,
            max_rounds=self.rounds,
        )

        print(f"\n💬 Debate Topic: {self.topic}\n")
        for i in range(self.rounds):
            state = side_a_node(state, debate_system=self)
            print(state.history[-1])
            state = side_b_node(state, debate_system=self)
            print(state.history[-1])
            state.round += 1

        # Judge's verdict
        verdict = judge_node(state, debate_system=self)
        print("\nJUDGE'S VERDICT:")
        print(verdict["verdict"])

if __name__ == "__main__":
    debate = LangGraphDebateSystem(
        topic="cats vs dogs",
        side_a_point="cats are better pets",
        side_b_point="dogs are better pets",
        rounds=2
    )
    debate.run_debate()
