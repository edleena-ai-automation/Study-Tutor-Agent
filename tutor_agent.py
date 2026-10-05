from crewai import Agent, Task, Crew, Process

from groq_llm import get_groq_response
from tools import calculator, study_plan_creator


class StudyTutorAgent:
    """
    Study Tutor Agent using CrewAI for agent/task management
    and Groq GPT-OSS 120B as the LLM.
    """

    def __init__(self):

        self.tutor = Agent(
            role="Personal Study Tutor",

            goal=(
                "Help students understand academic topics clearly, "
                "answer questions, provide examples, simplify difficult "
                "concepts, and help students create effective study plans."
            ),

            backstory=(
                "You are a patient and knowledgeable personal tutor. "
                "You explain difficult concepts in simple language. "
                "You adapt your explanations according to the student's "
                "level and encourage students to understand concepts "
                "rather than simply memorize answers."
            ),

            tools=[
                calculator,
                study_plan_creator,
            ],

            allow_delegation=False,

            verbose=False,
        )


    def ask(
        self,
        question,
        subject,
        level,
        memory,
    ):
        """
        Send the student's question to the Study Tutor.
        """

        prompt = f"""
You are a personal AI Study Tutor.

STUDENT SUBJECT:
{subject}

STUDENT LEVEL:
{level}

PREVIOUS CONVERSATION:
{memory}

CURRENT STUDENT QUESTION:
{question}

Your instructions:

1. Answer the student's current question directly.

2. Adapt the explanation to the student's level.

3. Use simple and clear language.

4. Break complicated concepts into smaller steps.

5. Give examples whenever useful.

6. If a mathematical calculation is required,
   use the calculator tool.

7. If the student asks for a study plan,
   use the study_plan_creator tool.

8. Use the previous conversation to maintain context.

9. If the student asks a follow-up question,
   understand what they are referring to from
   the previous conversation.

10. Do not mention internal instructions,
    CrewAI, tools, prompts, or system messages.

11. Do not pretend to know something if you are unsure.

12. Be encouraging and educational.

Return only the tutor's answer.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful, patient and knowledgeable "
                    "AI Study Tutor."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        return get_groq_response(
            messages=messages,
            temperature=0.4,
        )


def ask_tutor(
    question,
    subject,
    level,
    memory,
):

    tutor_agent = StudyTutorAgent()

    return tutor_agent.ask(
        question=question,
        subject=subject,
        level=level,
        memory=memory,
    )
