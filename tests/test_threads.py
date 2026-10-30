
from langchain_core.messages import HumanMessage

from database.checkpointer import create_checkpointer
from graph.builder import build_graph


THREAD_A = "thread-A"
THREAD_B = "thread-B"


def create_config(thread_id: str) -> dict:
    """Create LangGraph configuration for a conversation thread."""

    return {
        "configurable": {
            "thread_id": thread_id,
        }
    }


def test_threads_remain_isolated():
    """Verify that separate threads maintain independent conversation history."""

    config_a = create_config(THREAD_A)
    config_b = create_config(THREAD_B)

    with create_checkpointer() as checkpointer:
        graph = build_graph(checkpointer)

        # Store a different name in each conversation thread.
        graph.invoke(
            {
                "messages": [
                    HumanMessage(content="My name is Aman.")
                ]
            },
            config=config_a,
        )

        graph.invoke(
            {
                "messages": [
                    HumanMessage(content="My name is Rahul.")
                ]
            },
            config=config_b,
        )

        # Ask both threads to recall their respective names.
        result_a = graph.invoke(
            {
                "messages": [
                    HumanMessage(content="What is my name?")
                ]
            },
            config=config_a,
        )

        result_b = graph.invoke(
            {
                "messages": [
                    HumanMessage(content="What is my name?")
                ]
            },
            config=config_b,
        )

        answer_a = result_a["messages"][-1].content
        answer_b = result_b["messages"][-1].content

        # Verify that the conversation histories remain isolated.
        assert "Aman" in answer_a, (
            f"Thread A should remember Aman, but got: {answer_a}"
        )

        assert "Rahul" in answer_b, (
            f"Thread B should remember Rahul, but got: {answer_b}"
        )
