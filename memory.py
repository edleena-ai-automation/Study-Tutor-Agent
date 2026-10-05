import streamlit as st


def initialize_memory():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def add_message(role: str, content: str):
    st.session_state.chat_history.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_memory_text(max_messages: int = 10) -> str:

    history = st.session_state.chat_history[-max_messages:]

    if not history:
        return "No previous conversation."

    memory_text = []

    for message in history:
        role = message["role"].upper()
        content = message["content"]

        memory_text.append(
            f"{role}: {content}"
        )

    return "\n\n".join(memory_text)


def clear_memory():
    st.session_state.chat_history = []
