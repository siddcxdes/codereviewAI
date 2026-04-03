from database.db import Base, engine
import time

print("Dropping existing tables in database...")
Base.metadata.drop_all(bind=engine)
time.sleep(2)
print("Creating tables in database with new schema...")
Base.metadata.create_all(bind=engine)
print("Tables recreated successfully!")
