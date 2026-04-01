from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.webhook import router as webhook_router
from pydantic import BaseModel
from services.github_service import get_pr_files
from services.review_service import run_full_review

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "CodeReview AI is running!"}

class ManualReviewRequest(BaseModel):
    repo_name: str
    pr_number: int

@app.post("/api/analyze")
async def analyze_pr_manual(request: ManualReviewRequest):
    print(f"\nManual analysis requested!")
    print(f"Repo: {request.repo_name}")
    print(f"PR #{request.pr_number}")
    
    print(f"\nFetching changed files...")
    changed_files = get_pr_files(request.repo_name, request.pr_number)
    
    if not changed_files:
        return {"status": "error", "message": "No files found or unable to access PR (is it private?)."}
        
    print(f"\nRunning AI review...")
    review_data = run_full_review(changed_files)
    
    return {
        "status": "success",
        "data": review_data
    }