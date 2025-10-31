
"""
defines database models for el chefe

each class = database table:
    -user: stores user information (username, goals).
    -goal: stores goals linked to users.
    -task: stores Ai gen task linked to goals.

Relationship-
    -one user - many goals
    -one goal - many task
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.database import Base


#user table
"""Stores user information"""

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")

    """(__repr__)special method/dunder method: to return a string representation of an object 
        mostly for debugging/logging looks nice 
    """
    def __repr__(self):
        return f"<user(username={self.username}>"

#goal table
class Goal(Base):
    __tablename__= "goals"

    id =Column(Integer, primary_key=True, index=True)
    title =Column(String, nullable=False)
    description =Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #Relationship back to user
    user = relationship("User", back_populates="goals")

    #if tasks already exist
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

    completed = Column(Boolean, default=False)
    boss = Column(String, default="No BOSS Assigned")
    color = Column(String, default="#38bdf8")


#task table
"""stores ai gen tasks linked to goal"""
class Task(Base):
    __tablename__= "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description =Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    difficulty_stage = Column(Integer, nullable=True)

    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    goal = relationship("Goal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description={self.description}, stage={self.difficulty_stage} goal_id{self.goal_id})>"