
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

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    goals = relationship("Goal", back_populates="user", foreign_keys="Goal.user_id")
    bosses = relationship("Boss", back_populates="user")

    """(__repr__)special method/dunder method: to return a string representation of an object 
        mostly for debugging/logging looks nice 
    """
    def __repr__(self):
        return f"<user(username={self.username}>"

#boss tabel
class Boss(Base):
    __tablename__="bosses"

    id = Column(Integer, primary_key=True, index=True)
    name =Column(String, nullable=False, unique=True)
    strictness = Column(Integer, default=5)
    description = Column(String, default="")

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="bosses")
    goals = relationship("Goal", back_populates="boss_obj")


#goal table
class Goal(Base):
    __tablename__= "goals"

    id =Column(Integer, primary_key=True, index=True)
    title =Column(String, nullable=False)
    description =Column(String)

    #one foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    #one foreign key to boss
    boss_id = Column(Integer, ForeignKey("bosses.id"), nullable=False)



    #relationship
    user = relationship("User", back_populates="goals", foreign_keys=[user_id])
    boss_obj = relationship("Boss", back_populates="goals", foreign_keys=[boss_id])
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

    completed = Column(Boolean, default=False)
    color = Column(String, default="#38bdf8")


#task table
"""stores ai gen tasks linked to goal"""
class Task(Base):
    __tablename__= "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description =Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    difficulty_stage = Column(Integer, nullable=False, default=0)

    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    goal = relationship("Goal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description={self.description}, stage={self.difficulty_stage} goal_id{self.goal_id})>"


def get_default_boss(db):
    boss = db.query(Boss).filter(Boss.name =="Sensei Wu").first()
    if not boss:
        boss = Boss(name="Sensei Wu", strictness=5, description="Your are a wise mentor.")
        db.add(boss)
        db.commit()
        db.refresh(boss)
    return boss