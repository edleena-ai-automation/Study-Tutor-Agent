import os
from typing import Any

from groq import Groq
from crewai.llms.base_llm import BaseLLM


class GroqLLM(BaseLLM):
    """
    Simple CrewAI-compatible LLM wrapper for Groq.
    """

    model: str = "openai/gpt-oss-120b"
    temperature: float = 0.4
    provider: str = "groq"

    def call(
        self,
        messages: Any,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ) -> str:

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set.")

        client = Groq(api_key=api_key)

        # Convert CrewAI messages into Groq format
        if isinstance(messages, str):
            groq_messages = [
                {
                    "role": "user",
                    "content": messages,
                }
            ]
        else:
            groq_messages = []

            for message in messages:
                if isinstance(message, dict):
                    role = message.get("role", "user")
                    content = message.get("content", "")

                    groq_messages.append(
                        {
                            "role": role,
                            "content": content,
                        }
                    )

        response = client.chat.completions.create(
            messages=groq_messages,
            model=self.model,
            temperature=self.temperature,
        )

        return response.choices[0].message.content

    def supports_function_calling(self) -> bool:
        return False
