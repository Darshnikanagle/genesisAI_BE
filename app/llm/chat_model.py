from langchain.chat_models import init_chat_model
import os
from app.util import llm as model

from langchain_core.messages import HumanMessage, AIMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, trim_messages
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List

try:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    

    class State(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]
        language: str

    # Define the function that calls the model
    def call_model(state: State):
        prompt = prompt_template.invoke(state)
        response = model.invoke(prompt)
        return {"messages": [response]}

    trimmer = trim_messages(
        max_tokens=65,
        strategy="last",
        token_counter=model,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    # Define a new graph
    workflow = StateGraph(state_schema=State)


    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    

except Exception as e:
     print(f"An unexpected error occurred: {e}")

def chat(query: str, thread_id: int, messages: List[str] = None):
    try:
        # messages = [
        #     SystemMessage(content="you're a good assistant"),
        #     HumanMessage(content="hi! I'm bob"),
        #     AIMessage(content="hi!"),
        #     HumanMessage(content="I like vanilla ice cream"),
        #     AIMessage(content="nice"),
        #     HumanMessage(content="whats 2 + 2"),
        #     AIMessage(content="4"),
        #     HumanMessage(content="thanks"),
        #     AIMessage(content="no problem!"),
        #     HumanMessage(content="having fun?"),
        #     AIMessage(content="yes!"),
        # ]

        # trimmer.invoke(messages)

        config = {"configurable": {"thread_id": thread_id}} # this is to inform about the thread
        # query = "What was my last question?"
        language = "English"

        if messages:
            input_messages = messages + [HumanMessage(query)]
        else:
            input_messages = [HumanMessage(query)]

        output = app.invoke({"messages": input_messages, "language": language}, config)
        output["messages"][-1].pretty_print()  # output contains all messages in state
        return output["messages"][-1].content

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
