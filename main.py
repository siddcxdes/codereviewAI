from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
from routes.webhook import router as webhook_router
from pydantic import BaseModel
from services.github_service import get_pr_files
from services.review_service import run_full_review
from sqlalchemy.orm import Session
from database.db import get_db
from database import crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)


app.mount("/src", StaticFiles(directory="frontend/src"), name="src")

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")


class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/api/signup")
def signup(req: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(crud.User).filter(crud.User.username == req.username).first()
    if user:
        return {"status": "error", "message": "Username already exists."}
    new_user = crud.create_user(db, req.username, req.password)
    return {"status": "success", "token": new_user.token, "username": new_user.username}

@app.post("/api/login")
def login(req: AuthRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, req.username, req.password)
    if not user:
        return {"status": "error", "message": "Invalid credentials."}
    return {"status": "success", "token": user.token, "username": user.username}

@app.get("/api/history")
def get_history(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    user = crud.get_user_by_token(db, token)
    if not user:
        return {"status": "error", "message": "Unauthorized"}
    reviews = crud.get_user_reviews(db, user.id)
    return {
        "status": "success", 
        "history": [{
            "id": r.id, 
            "repo_name": r.repo_name, 
            "pr_number": r.pr_number, 
            "pr_title": r.pr_title, 
            "grade": r.grade, 
            "score": r.score, 
            "created_at": r.created_at
        } for r in reviews]
    }

class ManualReviewRequest(BaseModel):
    repo_name: str
    pr_number: int

@app.post("/api/analyze")
async def analyze_pr_manual(request_data: ManualReviewRequest, request: Request, db: Session = Depends(get_db)):
    print(f"\nManual analysis requested!")
    
    # Enforce Auth
    token = request.headers.get("Authorization")
    user = crud.get_user_by_token(db, token) if token else None
    if not user:
        return {"status": "error", "message": "Access Denied. You must be logged in to analyze a PR."}
    print(f"Repo: {request_data.repo_name}")
    print(f"PR #{request_data.pr_number}")
    
    print(f"\nFetching changed files...")
    changed_files = get_pr_files(request_data.repo_name, request_data.pr_number)
    
    if not changed_files:
        return {"status": "error", "message": "No files found or unable to access PR (is it private?)."}
        
    print(f"\nRunning AI review...")
    review_data = run_full_review(changed_files)
    
    # Save to history if user is logged in
    token = request.headers.get("Authorization")
    user = crud.get_user_by_token(db, token) if token else None
    user_id = user.id if user else None
    
    pr_title = f"PR #{request_data.pr_number}"
    crud.save_review(db, request_data.repo_name, request_data.pr_number, pr_title, review_data, user_id=user_id)
    
    return {
        "status": "success",
        "data": review_data
    }
