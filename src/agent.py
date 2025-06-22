from tools.tools import get_all_jikan_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
from rich.console import Console
from rich.markdown import Markdown
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv()


def load_memory():
    cs = os.getenv("MONGO_URI")
    client = MongoClient(cs)
    checkpointer = MongoDBSaver(client)

    return checkpointer


def WeeabooBudddy():
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    search = TavilySearchResults(max_results=2)
    tools = get_all_jikan_tools()
    tools.append(search)

    memory = load_memory()

    agent = create_react_agent(model, tools, checkpointer=memory)

    return agent


# Agent Conversation Tool
def talk_tuah():
    console = Console()
    agent = WeeabooBudddy()

    hi = input("Enter your question: ")
    config = {"configurable": {"thread_id": "abc123"}}
    for step in agent.stream(
        {"messages": [HumanMessage(content=hi)]},
        config,  # type: ignore
        stream_mode="values",
    ):
        if step["messages"][-1].type == "ai":
            m = step["messages"][-1].content
            content = Markdown(m)
            console.print(content)


if __name__ == "__main__":
    talk_tuah()
