from core.database import Base, engine
from routers import models

print("recreating Database ....")
Base.metadata.create_all(bind=engine)
print("Database created Successfully!")