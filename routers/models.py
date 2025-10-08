
"""
defines database models for el chefe

each class = database table:
    -profile: stores user information (username, goals).
    -goal: stores goals linked to profiles.
    -task: stores Ai gen task linked to goals.

Relationship-
    -one profile - many goals
    -one goal - many task
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


#profile table
"""Stores user profile information"""

class Profile(Base):
    __tablename__= "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    goals = relationship("Goal", back_populates="profile", cascade="all, delete-orphan")

    """(__repr__)special method/dunder method: to return a string representation of an object 
        mostly for debugging/logging looks nice 
    """
    def __repr__(self):
        return f"<Profile(username={self.username}>"

#goal table
class Goal(Base):
    __tablename__= "goals"

    id =Column(Integer, primary_key=True, index=True)
    title =Column(String, index=True)
    description =Column(String, nullable=True)
    boss = Column(String, default="default") #stores selected boss
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="goals")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

#task table
"""stores ai gen tasks linked to goal"""
class Task(Base):
    __tablename__= "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description =Column(String, index=True)
    goal_id =Column(Integer, ForeignKey("goals.id"))

    goal = relationship("Goal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description={self.description}, goal_id{self.goal_id})>"