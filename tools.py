from crewai.tools import tool


@tool("calculator")
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Use this tool when the student asks for a mathematical calculation.
    Example: 25 * 4
    """

    try:
        allowed_characters = "0123456789+-*/().% "

        if not all(char in allowed_characters for char in expression):
            return "I can only calculate basic mathematical expressions."

        result = eval(expression, {"__builtins__": {}}, {})

        return f"Calculation result: {result}"

    except Exception:
        return "I could not calculate that expression."


@tool("study_plan_creator")
def study_plan_creator(topic: str, days: int) -> str:
    """
    Create a simple study schedule for a topic.

    Use this when the student asks for a study plan.
    """

    if days < 1:
        days = 1

    if days > 30:
        days = 30

    plan = []

    for day in range(1, days + 1):
        if day == 1:
            activity = f"Learn the fundamentals of {topic}."
        elif day == days:
            activity = f"Review {topic} and test yourself."
        else:
            activity = f"Study and practice {topic}."

        plan.append(f"Day {day}: {activity}")

    return "\n".join(plan)
