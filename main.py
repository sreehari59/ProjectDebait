import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# Define types

class DebateResponse:
    def __init__(self, author: str, message: str):
        self.author = author
        self.message = message
    def __str__(self):
        return f"DebateResponse by {self.author}: \"{self.message}\""
    def __repr__(self):
        return self.__str__()

def response_reducer(left: list[DebateResponse], right: list[DebateResponse]) -> list[DebateResponse]:
    return left + right

class DebateState(TypedDict):
    responses: Annotated[list[DebateResponse], response_reducer]


# Setup LLM

load_dotenv()

mistral = ChatOpenAI(
    openai_api_base="https://api.mistral.ai/v1",
    openai_api_key=os.getenv("MISTRAL_API_KEY"),
    model="mistral-large-latest",
    temperature=0.0,
)

openAi = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.0,
)

llm = mistral


# Setup debate graph

def debate(name: str, prompt: str, state: DebateState):
    response = llm.invoke([
        ("system", f"You are debate agent {name}. Respond in a very concise manner. The shorter the better."),
        ("human", prompt),
    ])
    return { "responses": [DebateResponse(author=name, message=response.content)] }

def debater1(state: DebateState):
    return debate(
        name="Cat Person", 
        prompt="You are debating 'Cats vs. Dogs'. Provide a single argument why Cats are better.", 
        state=state)

def debater2(state: DebateState):
    return debate(
        name="Dog Person", 
        prompt="You are debating 'Cats vs. Dogs'. Provide a single argument why Dogs are better.",
        state=state)

def judge(state: DebateState):
    response = llm.invoke([
        ("system", "You are a debate judge. Respond in a very concise manner. The shorter the better."),
        *[("human", f"{response.author}: {response.message}") for response in state["responses"]],
        ("human", "What side provided the better argument? Respond with 'Cats' or 'Dogs'."),
    ])
    return { "responses": [DebateResponse("judge", response.content)] }

graph_builder = StateGraph(DebateState)

graph_builder.add_edge(START, "debater1")
graph_builder.add_node("debater1", debater1)
graph_builder.add_edge("debater1", "debater2")
graph_builder.add_node("debater2", debater2)
graph_builder.add_edge("debater2", "judge")
graph_builder.add_node("judge", judge)
graph_builder.add_edge("judge", END)

debate_graph = graph_builder.compile()

png = debate_graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png)


# Run the debate

for event in debate_graph.stream(DebateState()):
    for value in event.values():
        for response in value["responses"]:
            print(response)
