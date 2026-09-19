import json
from groq import Groq
from ..core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_trip_plan(destination: str,days: int,interests: str) -> str:

    prompt = f"""
Create a practical travel itinerary.

Destination: {destination}
Number of days: {days}
Interests: {interests}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Short summary of the trip",
    "days": [
        {{
            "day": 1,
            "title": "Title of the day",
            "activities": [
                "Activity 1",
                "Activity 2",
                "Activity 3"
            ],
            "food": [
                "Food recommendation 1",
                "Food recommendation 2"
            ],
            "tips": [
                "Travel tip 1",
                "Travel tip 2"
            ]
        }}
    ]
}}

Rules:

- Create exactly {days} day objects.
- The "day" field must contain the day number.
- "title" should describe the main focus of that day.
- "activities" should contain important places and things to do.
- "food" should contain useful local food recommendations.
- "tips" should contain practical travel advice.
- Make the itinerary realistic.
- Consider the user's interests.
- Do not include markdown.
- Do not include code fences.
- Do not include any text outside the JSON.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful travel-planning assistant. "
                    "Return only valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError("AI returned an invalid travel plan format")