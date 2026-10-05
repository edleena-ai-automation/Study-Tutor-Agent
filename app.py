import streamlit as st

from memory import (
    initialize_memory,
    add_message,
    get_memory_text,
    clear_memory,
)

from tutor_agent import ask_tutor


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🎓",
    layout="wide",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(0, 153, 255, 0.18),
                transparent 35%
            ),
            radial-gradient(
                circle at bottom left,
                rgba(0, 255, 255, 0.10),
                transparent 30%
            ),
            #07111f;
        color: #f8fafc;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #38bdf8,
            #22d3ee,
            #60a5fa
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .info-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow:
            0 0 30px rgba(14, 165, 233, 0.08);
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        background: linear-gradient(
            135deg,
            #0284c7,
            #2563eb
        );
        color: white;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #67e8f9;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# MEMORY INITIALIZATION
# --------------------------------------------------

initialize_memory()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 Study Tutor AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI tutor for learning, practice and study planning.'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎯 Study Settings")

    subject = st.selectbox(
        "Subject",
        [
            "General",
            "Chemistry",
            "Biology",
            "Physics",
            "Mathematics",
            "Computer Science",
            "English",
            "History",
        ],
    )

    level = st.selectbox(
        "Your Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    st.divider()

    st.markdown("### 🧠 Memory")

    st.caption(
        "The tutor remembers the conversation during your current session."
    )

    if st.button("🗑️ Clear Conversation"):
        clear_memory()
        st.rerun()

    st.divider()

    st.markdown("### 💡 Try asking")

    st.caption("Explain photosynthesis simply.")

    st.caption("Make me a study plan for organic chemistry.")

    st.caption("Calculate 25 × 18.")

    st.caption("Quiz me on Newton's laws.")


# --------------------------------------------------
# CHAT DISPLAY
# --------------------------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_question = st.chat_input(
    "Ask your Study Tutor anything..."
)


if user_question:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_question)

    add_message(
        "user",
        user_question,
    )

    # Get previous conversation
    memory = get_memory_text()

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("🧠 Your tutor is thinking..."):

            try:

                answer = ask_tutor(
                    question=user_question,
                    subject=subject,
                    level=level,
                    memory=memory,
                )

                st.markdown(answer)

                add_message(
                    "assistant",
                    answer,
                )

            except Exception as e:

                error_message = (
                    "Something went wrong while contacting the tutor.\n\n"
                    f"Error: `{str(e)}`"
                )

                st.error(error_message)
