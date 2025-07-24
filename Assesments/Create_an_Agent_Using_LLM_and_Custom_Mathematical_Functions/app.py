from langgraph.graph import StateGraph, END
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import TypedDict, List, Optional, Annotated, Union
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import operator

load_dotenv()

# --- LLM Initialization ---
llm_engine = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# --- State Definition ---
class DialogueState(TypedDict):
    history: Annotated[List[BaseMessage], operator.add]
    prompt: str
    result: Optional[Union[BaseMessage, List[tuple]]]
    steps: List

# --- Custom Math Tools ---
@tool
def add_numbers(x: float, y: float) -> float:
    """Returns the sum of x and y."""
    return x + y

@tool
def subtract_numbers(x: float, y: float) -> float:
    """Returns the result of x minus y."""
    return x - y

@tool
def multiply_numbers(x: float, y: float) -> float:
    """Returns the product of x and y."""
    return x * y

@tool
def safe_divide(x: float, y: float) -> float:
    """Divides x by y. Returns error if y is zero."""
    if y == 0:
        return "Error: Division by zero is undefined."
    return x / y

math_tools = [add_numbers, subtract_numbers, multiply_numbers, safe_divide]

# --- System Prompt ---
assistant_prompt = """You are CalcBot, a friendly digital assistant.
- For math, always use the provided tools.
- For general queries, answer using your own knowledge.
- Make your answers clear and concise.
"""

# --- Agent Construction ---
calc_agent = create_tool_calling_agent(
    llm=llm_engine,
    tools=math_tools,
    prompt=ChatPromptTemplate.from_messages([
        ("system", assistant_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]),
)

calc_executor = AgentExecutor(agent=calc_agent, tools=math_tools, verbose=True)

# --- Node Logic ---
def calc_node(state: DialogueState):
    agent_reply = calc_executor.invoke({
        "input": state["prompt"],
        "chat_history": state["history"]
    })
    return {
        "history": [AIMessage(content=agent_reply["output"])],
        "result": agent_reply["output"]
    }

# --- Graph Construction ---
dialogue_graph = StateGraph(DialogueState)
dialogue_graph.add_node("calc", calc_node)
dialogue_graph.set_entry_point("calc")
dialogue_graph.add_edge("calc", END)
compiled_graph = dialogue_graph.compile()

def interact_with_agent(user_text: str, chat_msgs: List[BaseMessage] = []):
    try:
        inputs = {
            "history": chat_msgs,
            "prompt": user_text
        }
        output = compiled_graph.invoke(inputs)
        return output["result"]
    except Exception as err:
        return f"Error: {str(err)}"

# --- CLI Chat Loop ---
if __name__ == "__main__":
    print("Welcome to CalcBot! Type 'exit' to leave.")
    chat_log = []
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue

            # Convert chat log to BaseMessage objects
            formatted_history = []
            for entry in chat_log:
                if entry["role"] == "user":
                    formatted_history.append(HumanMessage(content=entry["content"]))
                else:
                    formatted_history.append(AIMessage(content=entry["content"]))

            agent_response = interact_with_agent(user_input, formatted_history)

            chat_log.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": str(agent_response)}
            ])
            print(f"CalcBot: {agent_response}")

        except KeyboardInterrupt:
            break
        except Exception as err:
            print(f"Error: {str(err)}")