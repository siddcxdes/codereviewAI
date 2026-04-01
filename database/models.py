from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database.db import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, index=True)
    pr_number = Column(Integer)
    pr_title = Column(String)
    score = Column(Integer)
    grade = Column(String)
    full_comment = Column(Text)
    bugs_found = Column(Integer, default=0)
    security_issues = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)