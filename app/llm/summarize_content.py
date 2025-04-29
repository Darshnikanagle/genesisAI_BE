from langchain.chat_models import init_chat_model
import os

from app.util import llm as model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, trim_messages
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                # "You are a helpful and professional assistant. Summarize the given content clearly and concisely, highlighting only the most important points. Avoid unnecessary details. Use html tags like <br>, <Strong> to format the content.",
                """Generate a clean and readable summary based on the input content. 
                - Generate a clean and structured summary.
                - Each section heading should be wrapped inside a <h4> tag.
                - Each normal paragraph should be wrapped inside a <p> tag.
                - Lists should use <ul> and <li> tags.
                - Do not return <html>, <head>, or <body> tags.
                - Ensure the HTML is clean and properly closed.
                """
            ),
            ("user", "{text}"),
        ]
    )


def summarize_content(content):
    try:
        prompt = prompt_template.invoke({"text": content})

        output = model.invoke(prompt)
        print(output.content)  # output contains all messages in state

        return output.content

    except Exception as e:
     print(f"An unexpected error occurred: {e}")




