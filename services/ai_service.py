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
from routers import models


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

    prompt = f"""
    create **15 tasks** for the goal: "{goal.title}"
    
    Divide them into 3 difficulty groups: 
    - Tasks 1-5: Beginner level / getting started
    - Tasks 6-10: Intermediate difficulty
    - Tasks 11-15: Advanced / Mastery level
    
    Return them in a numbered list, like 
    1. first 1-5
    2. next 6-10 
    3. last 11-15
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
            "content": "you are a structured goal planning mentor, through my tasks of each goal, create small actionable tasks that help me learn my goal"},
            {"role": "user", "content": prompt}
        ]
    )

    raw_output = response.choices[0].message.content.strip()

    tasks =[
        line.split(".", 1)[1].strip() if "." in line else line.strip()
        for line in raw_output.split("\n")
        if line.strip()
    ]

    tasks = tasks[:15]

    for index, task_description in enumerate(tasks):
        difficulty_stage = index // 5

        new_task = models.Task(
            description=task_description,
            goal_id=goal.id,
            difficulty_stage=difficulty_stage,
            completed=False
        )
        db.add(new_task)

    db.commit()




