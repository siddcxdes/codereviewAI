from database.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    print("Adding user_id to reviews...")
    try:
        conn.execute(text("ALTER TABLE reviews ADD COLUMN user_id INTEGER REFERENCES users(id);"))
        conn.commit()
        print("Success!")
    except Exception as e:
        print(f"Error (might already exist): {e}")
