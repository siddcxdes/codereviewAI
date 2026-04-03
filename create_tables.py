from database.db import engine, Base
from database.models import Review, User

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
