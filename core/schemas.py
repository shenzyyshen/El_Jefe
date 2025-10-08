# schemas.py
"""
Pydantic models (schemas) for request/response validation
"""

from pydantic import BaseModel
from typing import List, Optional

""" 
goal 
"""

class GoalBase(BaseModel):
    """share fields for all goals"""
    title: str
    description: Optional[str] = None

class GoalCreate(GoalBase):
    """ for creating a new goal(input)"""
    pass

class Goal(GoalBase):
    """schema for reading  goal (input )"""
    id: int
    profile_id: int

    class Config:
        from_attributes = True
"""
profile 
"""

class ProfileBase(BaseModel):
    """shared fields for all profiles """
    username: str

class ProfileCreate(ProfileBase):
    """schema for creating a profile (input)"""
    goals: List[GoalCreate] = []

class Profile(ProfileBase):
    """schema for reading a profile (output)"""
    id: int
    goals: List[Goal] = []

    class Config:
        from_attributes = True

"""
task
"""

class TaskBase(BaseModel):
    """shared fields for all tasks"""
    description: str

class TaskCreate(TaskBase):
    """schema for creating a tas (input)"""
    pass

class Task(TaskBase):
    """schma for reading a task (output)"""
    id:int
    goal_id: int

    class Config:
        from_attributes = True

