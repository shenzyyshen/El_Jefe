from core.database import Base, engine
from routers import models

Base.metadata.create_all(bind=engine)
print("Database created!")