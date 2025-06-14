import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from typing import Literal, List
from pydantic import BaseModel, Field

class DebateState(BaseModel):
    history: List[str] = Field(default_factory=list)
    round: int = 0
    max_rounds: int = 2
    verdict: str = ""

class LangGraphDebateSystem:
    def __init__(self, topic, side_a_point, side_b_point, rounds=2):
        self.topic = topic
        self.side_a_point = side_a_point
        self.side_b_point = side_b_point
        self.rounds = rounds

        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_base=os.getenv("MISTRAL_OPENAI_API_BASE", "https://api.mistral.ai/v1"),
            openai_api_key=os.getenv("MISTRAL_API_KEY"),
            model="mistral-tiny",
            temperature=0.7,
        )

        # Define prompts
        self.prompts = {
            "side_a": PromptTemplate(
                input_variables=["point", "topic", "history"],
                template=
                "You are a passionate but professional debater arguing FOR: {point}.\n"
                "Debate topic: {topic}\n"
                "Context so far:\n{history}\n"
                "Provide one clear, concise argument. Keep it under 2 sentences. Be persuasive but professional."
                "Your argument:"
            ),
            "side_b": PromptTemplate(
                input_variables=["point", "topic", "history"],
                template=
                "You are a passionate but professional debater arguing FOR: {point}.\n"
                "Debate topic: {topic}\n"
                "Context so far:\n{history}\n"
                "Provide one clear, concise counterargument. Keep it under 2 sentences. Be persuasive but professional."
                "Your argument:"
            ),
            "judge": PromptTemplate(
                input_variables=["transcript", "topic"],
                template=
                "You are judging a debate on: {topic}.\n"
                "Debate transcript:\n{transcript}\n"
                "Provide your verdict in exactly this format:\n"
                "VERDICT: The [winning side] argument is more convincing because [one clear reason]"
            )
        }

        # Build workflow graph
        self._build_workflow()

    def _generate_response(self, state: DebateState, side: str) -> DebateState:
        """Generate debate response for either side A or B"""
        history_str = "\n".join(state.history)
        point = self.side_a_point if side == "side_a" else self.side_b_point

        msg = self.prompts[side].format(
            point=point,
            topic=self.topic,
            history=history_str
        )
        response = self.llm.invoke(msg)

        # Update state
        new_history = state.history + [f"{side}: {response.content.strip()}"]
        new_round = state.round + (1 if side == "side_b" else 0)

        return DebateState(
            history=new_history,
            round=new_round,
            max_rounds=state.max_rounds,
            verdict=state.verdict
        )

    def _generate_verdict(self, state: DebateState) -> DebateState:
        """Generate judge's verdict"""
        transcript = "\n".join(state.history)
        msg = self.prompts["judge"].format(
            topic=self.topic,
            transcript=transcript
        )
        verdict = self.llm.invoke(msg).content.strip()

        return DebateState(
            history=state.history + [verdict],
            round=state.round,
            max_rounds=state.max_rounds,
            verdict=verdict
        )

    def _build_workflow(self):
        # Create node functions
        def side_a_node(state): return self._generate_response(state, "side_a")
        def side_b_node(state): return self._generate_response(state, "side_b")
        def judge_node(state): return self._generate_verdict(state)

        # Define round completion condition
        def should_continue_debate(state: DebateState) -> Literal["continue", "end"]:
            return "continue" if state.round < state.max_rounds else "end"

        # Build the graph
        builder = StateGraph(DebateState)
        builder.add_node("side_a", side_a_node)
        builder.add_node("side_b", side_b_node)
        builder.add_node("judge", judge_node)

        # Connect nodes
        builder.add_edge("side_a", "side_b")
        builder.add_conditional_edges("side_b", should_continue_debate, {
            "continue": "side_a",
            "end": "judge"
        })

        builder.set_entry_point("side_a")
        builder.add_edge("judge", END)

        self.workflow = builder.compile()

    def run_debate(self):
        state = DebateState(
            history=[
                f"Topic: {self.topic}",
                f"Position A: {self.side_a_point}",
                f"Position B: {self.side_b_point}"
            ],
            round=0,
            max_rounds=self.rounds
        )

        final_state = self.workflow.invoke(state)
        return final_state

if __name__ == "__main__":
    debate = LangGraphDebateSystem(
        topic="Should remote work be the standard?",
        side_a_point="Remote work should be the standard employment model",
        side_b_point="Traditional office work should remain the standard",
        rounds=2
    )
    result = debate.run_debate()
    
    for message in result['history']:
        if message.startswith("side_a:"):
            print("🔵 " + message[7:])
        elif message.startswith("side_b:"):
            print("🔴 " + message[7:])
        elif message.startswith("VERDICT:"):
            print("\n⚖️ " + message)
        else:
            print("📝 " + message)