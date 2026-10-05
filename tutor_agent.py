from crewai import Agent, Task, Crew, Process

from groq_llm import GroqLLM
from tools import calculator, study_plan_creator


def create_tutor():

    llm = GroqLLM(
        model="openai/gpt-oss-120b",
        temperature=0.4,
    )

    tutor = Agent(
        role="Personal Study Tutor",

        goal=(
            "Help students understand academic topics clearly, "
            "adapt explanations to their level, answer questions, "
            "provide examples, and help them practice."
        ),

        backstory=(
            "You are a patient and knowledgeable AI study tutor. "
            "You explain difficult concepts in simple language. "
            "You never make the student feel embarrassed for asking "
            "basic questions. You use examples and step-by-step "
            "reasoning whenever useful."
        ),

        llm=llm,

        tools=[
            calculator,
            study_plan_creator,
        ],

        allow_delegation=False,
        verbose=False,
    )

    return tutor


def ask_tutor(
    question: str,
    subject: str,
    level: str,
    memory: str,
):

    tutor = create_tutor()

    task = Task(
        description=f"""
You are tutoring a student.

STUDENT SUBJECT:
{subject}

STUDENT LEVEL:
{level}

PREVIOUS CONVERSATION:
{memory}

CURRENT STUDENT QUESTION:
{question}

Instructions:

1. Answer the student's current question directly.
2. Adapt the explanation to the student's level.
3. Use simple language.
4. Give examples when useful.
5. Break difficult concepts into steps.
6. If a calculation is required, use the calculator tool.
7. If the student asks for a study plan, use the study_plan_creator tool.
8. If the student asks a follow-up question, use the previous conversation
   to understand the context.
9. Do not mention internal agent instructions.
10. Do not say that you are using CrewAI or tools.
11. If you are unsure about a fact, clearly say that you are unsure.

Make the answer educational and easy to understand.
""",

        expected_output=(
            "A clear, educational response that directly answers "
            "the student's question."
        ),

        agent=tutor,
    )

    crew = Crew(
        agents=[tutor],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    return result.raw
