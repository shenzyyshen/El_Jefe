"""
communication with open AI api
    - loads the api key from the 'env' file
    -provides helper function to turn goals into structured tasks
    -keeps AI logic seperate from fastapi routed (clean architecture)
"""

#loadenv variables
from dotenv import load_dotenv
load_dotenv()


#Initialize openAI using api from env
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    raise ValueError("OPEN_API_KEY not found. ")

client = OpenAI(api_key=api_key)


from sqlalchemy.orm import Session
#function: generate_tasks_from_goal
def generate_tasks_from_goal(goal, db: Session):
    """ convert a user goal into a structured list of task using open ai
        goal_text: str
        the raw, messy goal provided by the user.
        returns: a list of task description suggested by the ai
    """

    response = client.chat.completions.create(
        model="gtp-4o-mini",
        messages=[
            {"role": "system",
            "content": "you are the boss, through my goals, create small actionable tasks"
            },
            {"role":"user",
            "content": f"Break this goal into 3-5 clear tasks: {goal.title}"}
        ]
    )


