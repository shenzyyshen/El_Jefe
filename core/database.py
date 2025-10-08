
"""
database connection for the boss
- sqlalchemy is used as the ORM (object Relational mapper)
-sqlite is chosen for simplicity, but can be swapped with (postgreSQL or MYSQL)
-SessionLocal is used to create short-lived database session (per request)
-base = parent class zsed by all model (profile, Goal, task)
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#databse url
SQLALCHEMY_DATABASE_URL = "sqlite:///./eljefe.db"

#creates engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#sessionlocal - each request gets its own database session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for all models
Base = declarative_base()