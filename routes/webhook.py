from fastapi import APIRouter, Request
from services.github_service import get_pr_files, post_pr_comment
from services.review_service import run_full_review

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if "pull_request" not in payload:
        return {"status": "ignored"}
    
    action = payload.get("action", "")
    
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored"}
    pr = payload["pull_request"]
    pr_number = pr["number"]
    repo_name = payload["repository"]["full_name"]
    pr_title = pr["title"]
    
    print(f"\nNew PR received!")
    print(f"Repo: {repo_name}")
    print(f"PR #{pr_number}: {pr_title}")
    
    print(f"\nFetching changed files...")
    changed_files = get_pr_files(repo_name, pr_number)
    
    if not changed_files:
        post_pr_comment(repo_name, pr_number, "CodeReview AI: No code files found to review.")
        return {"status": "no files found"}
    print(f"\nRunning AI review...")
    review_data = run_full_review(changed_files)
    print(f"\nPosting comment on PR...")
    post_pr_comment(repo_name, pr_number, review_data["comment"])
    
    return {"status": "review posted successfully"}