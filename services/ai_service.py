"""
communication with open AI api
    - loads the api key from the 'env' file
    -provides helper function to turn goals into structured tasks
    -keeps AI logic seperate from fastapi routed (clean architecture)
"""


#Initialize openAI using api from env
import os
import re
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session
from routers import models

#loadenv variables
load_dotenv()

api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    raise ValueError("OPEN_API_KEY not found in environment variables. ")

#initialize openai client
client = OpenAI(api_key=api_key)

#function: generate_tasks_from_goal
def generate_tasks_from_goal(goal, db: Session, num_tasks: int =15):
    """
    convert a user goal into 15 structured list of task using open ai
        tasks are flavored according to the assigned boss.
        divided into 3 difficulty groups of 5 tasks each:
        -beginner : 1-5
        -intermediate: 6-10
        -advanced: 11-15
    """
    #get boss info
    try:
        boss_name = goal.boss_obj.name if goal.boss_obj else "Generic Boss"
        boss_desc = goal.boss_obj.description if goal.boss_obj else "Neutral Mentor"

        prompt = f"""
    You are an Ai goal mentor.
    Generate {num_tasks} actionable tasks** for the goal titled: "{goal.title}"
    goal description: "{goal.description or ''}"
    Boss: {boss_name} ({boss_desc})
    The tasks should reflect the personality of the Boss -funny, strict, motivating, etc.
    Do NOT include any headers, titles, comments, or repeated goal/boss info.
    return exactly 15 tasks in a numbered list (1-15), each task on its own line.
    
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
                {
                    "role": "system",
                "content": "you are a structured goal planning mentor, through my tasks of each goal, create small actionable tasks that help me learn my goal"
                },
                {"role": "user", "content": prompt}
            ]
        )

        raw_output = response.choices[0].message.content.strip()

        tasks =[]
        for line in raw_output.split("\n"):
            match = re.match(r"^\d+\.\s*(.+)$", line.strip())
            if match:
                tasks.append(match.group(1).strip())

    #limit to the number of tasks requested
        tasks = tasks[:num_tasks]

        for index, task_description in enumerate(tasks):
            difficulty_stage = index // (num_tasks // 3)
            new_task = models.Task(
                description=task_description,
                goal_id=goal.id,
                difficulty_stage=difficulty_stage,
                completed=False
            )
            db.add(new_task)

        db.commit()

    except Exception as e:
        print("AI Task generation failed:", e)
        traceback.print_exc()




