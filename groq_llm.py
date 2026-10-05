import os
from groq import Groq


MODEL_NAME = "openai/gpt-oss-120b"


def get_groq_client():
    """
    Create and return a Groq client using the API key
    stored in Streamlit secrets or environment variables.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def get_groq_response(messages, temperature=0.4):
    """
    Send messages to Groq and return the AI response.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content
