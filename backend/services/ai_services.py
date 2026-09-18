from groq import Groq
from ..core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_trip_plan(destination: str,days: int,interests: str) -> str:

    prompt = f"""
    Create a practical travel itinerary.

    Destination: {destination}
    Number of days: {days}
    Interests: {interests}

    Include:
    - Day-by-day plan
    - Important places to visit
    - Food recommendations
    - Practical travel tips

    Keep the response clear and useful.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful travel-planning assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content