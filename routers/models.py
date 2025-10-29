
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
"""Stores user user information"""

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
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
    title =Column(String, index=True)
    description =Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    boss = Column(String, default="default") #stores selected boss

    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

#task table
"""stores ai gen tasks linked to goal"""
class Task(Base):
    __tablename__= "tasks"

    id = Column(Integer, primary_key=True, index=True)
    goal_id =Column(Integer, ForeignKey("goals.id"))
    description =Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    goal = relationship("Goal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description={self.description}, goal_id{self.goal_id})>"