from database.db import engine, Base
from database.models import Review

print("Creating tables in database...")

Base.metadata.create_all(bind=engine)

print(" Tables created successfully!")