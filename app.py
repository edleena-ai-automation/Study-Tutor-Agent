import streamlit as st

from memory import (
    initialize_memory,
    add_message,
    get_memory_text,
    clear_memory,
)

from tutor_agent import ask_tutor


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 191, 255, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 90%,
                rgba(0, 102, 255, 0.12),
                transparent 30%
            ),
            #07111f;
    }


    /* Main content */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* Header */

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;

        background: linear-gradient(
            90deg,
            #38bdf8,
            #22d3ee,
            #60a5fa
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 5px;
    }


    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }


    /* Cards */

    .feature-card {
        background: rgba(15, 23, 42, 0.75);

        border: 1px solid rgba(
            56,
            189,
            248,
            0.20
        );

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 0 25px rgba(
                14,
                165,
                233,
                0.06
            );
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #081526,
                #050d18
            );

        border-right:
            1px solid rgba(
                56,
                189,
                248,
                0.15
            );
    }


    /* Buttons */

    .stButton > button {

        width: 100%;

        border-radius: 12px;

        border:
            1px solid rgba(
                56,
                189,
                248,
                0.35
            );

        background:
            linear-gradient(
                135deg,
                #0284c7,
                #2563eb
            );

        color: white;

        font-weight: 700;

        transition: 0.2s;
    }


    .stButton > button:hover {

        border-color: #67e8f9;

        box-shadow:
            0 0 20px rgba(
                34,
                211,
                238,
                0.25
            );
    }


    /* Chat input */

    div[data-testid="stChatInput"] {

        border-color:
            rgba(
                56,
                189,
                248,
                0.3
            );
    }


    /* Select boxes */

    div[data-baseweb="select"] > div {

        background-color:
            rgba(
                15,
                23,
                42,
                0.8
            );

        border-radius: 10px;
    }


    /* Divider */

    hr {

        border-color:
            rgba(
                56,
                189,
                248,
                0.12
            );
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# INITIALIZE MEMORY
# ==================================================

initialize_memory()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🎓 Study Tutor")

    st.caption(
        "Your personal AI learning assistant"
    )

    st.divider()


    # Subject

    subject = st.selectbox(
        "📚 Subject",

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


    # Student level

    level = st.selectbox(
        "🎯 Your Level",

        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )


    st.divider()


    # Memory section

    st.markdown("### 🧠 Conversation Memory")

    st.caption(
        "Your tutor remembers the conversation "
        "during the current session."
    )


    if st.button(
        "🗑️ Clear Conversation"
    ):

        clear_memory()

        st.rerun()


    st.divider()


    # Example questions

    st.markdown("### 💡 Try asking")

    st.caption(
        "Explain hybridization in simple words."
    )

    st.caption(
        "Make me a 7-day study plan for chemistry."
    )

    st.caption(
        "Calculate 25 × 18."
    )

    st.caption(
        "Quiz me about Newton's laws."
    )


# ==================================================
# MAIN HEADER
# ==================================================

st.markdown(
    '<div class="hero-title">'
    '🎓 Study Tutor AI'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    'Learn smarter. Ask questions. Understand concepts.'
    '</div>',
    unsafe_allow_html=True,
)


# ==================================================
# WELCOME CARD
# ==================================================

if len(st.session_state.chat_history) == 0:

    st.markdown(
        """
        <div class="feature-card">

        <h3>👋 Welcome to Study Tutor</h3>

        <p>
        Ask me anything about your subject.
        I can explain difficult concepts,
        provide examples, help with calculations,
        and create study plans.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# CHAT INPUT
# ==================================================

user_question = st.chat_input(
    "Ask your Study Tutor anything..."
)


# ==================================================
# PROCESS QUESTION
# ==================================================

if user_question:

    # -------------------------------
    # Display user message
    # -------------------------------

    with st.chat_message("user"):

        st.markdown(
            user_question
        )


    # Save user message

    add_message(
        "user",
        user_question,
    )


    # -------------------------------
    # Get conversation memory
    # -------------------------------

    memory = get_memory_text(
        max_messages=10
    )


    # -------------------------------
    # Generate tutor response
    # -------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Your tutor is thinking..."
        ):

            try:

                answer = ask_tutor(
                    question=user_question,
                    subject=subject,
                    level=level,
                    memory=memory,
                )

                st.markdown(
                    answer
                )


                # Save AI response

                add_message(
                    "assistant",
                    answer,
                )


            except Exception as e:

                st.error(
                    "⚠️ Something went wrong."
                )

                st.caption(
                    f"Error details: {str(e)}"
                )
