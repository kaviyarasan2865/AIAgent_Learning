from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.agents.tools import Tool
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any, TypedDict
import os

os.environ["GOOGLE_API_KEY"] = "your-google-api-key"

# LangChain agent with Gemini
@tool
def sum_tool(numbers: str) -> str:
    """Returns the sum of two numbers provided as 'a,b'."""
    try:
        a, b = map(int, numbers.split(","))
        return str(a + b)
    except:
        return "Please provide input like '5,10'."

tools = [
    Tool(
        name="sum_tool",
        func=sum_tool,
        description="Use this to add two numbers given as a string like '5,10'"
    )
]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# LangGraph wrapper
class AgentState(TypedDict):
    input: str
    output: Any

def agent_node(state: AgentState) -> AgentState:
    state["output"] = agent.run(state["input"])
    return state

# Build LangGraph
graph = StateGraph(AgentState)
graph.add_node("agent_node", agent_node)
graph.set_entry_point("agent_node")
app = graph.compile()

# Input should be natural language
initial_state = AgentState(
    input="What is the sum of 5 and 10?",
    output=None
)

# Run the graph
result = app.invoke(initial_state)

print("\n=== Final Output ===")
print(result)
