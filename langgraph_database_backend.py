from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import sqlite3

load_dotenv()

llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)

## State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

## CheckPointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

response=chatbot.invoke(
                {'messages': [HumanMessage(content= 'Hi my name is saif')]},
                    config=CONFIG
            )

print(chatbot.get_state(config=CONFIG).values['messages'])

## test
CONFIG = {'configurable': {'thread_id':'thread-1'}}

response=chatbot.invoke(
                {'messages': [HumanMessage(content='what is my name')]},
                    config=CONFIG
            )
print(response)



