from database.models import Review
from sqlalchemy.orm import Session


def save_review(db: Session, repo_name: str, pr_number: int, pr_title: str, review_data: dict):
    score_data = review_data.get("score", {})
    bugs_found = 0
    security_issues = 0

    for file_result in review_data.get("results", []):
        bug_issues = file_result.get("bug_detection", {}).get("issues", [])
        bugs_found += len(bug_issues)
        sec_issues = file_result.get("security_scan", {}).get("issues", [])
        security_issues += len(sec_issues)

    new_review = Review(
        repo_name=repo_name,
        pr_number=pr_number,
        pr_title=pr_title,
        score=score_data.get("total_score", 0),
        grade=score_data.get("grade", "N/A"),
        full_comment=review_data.get("comment", ""),
        bugs_found=bugs_found,
        security_issues=security_issues
    )

    db.add(new_review)
    
    db.commit()
    
    print(f"Review saved to database!")
    
    return new_review


def get_all_reviews(db: Session):
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    
    return reviews


def get_stats(db: Session):
    all_reviews = db.query(Review).all()
    total_prs = len(all_reviews)
    total_bugs = sum(r.bugs_found for r in all_reviews)
    total_security = sum(r.security_issues for r in all_reviews)
    
    if total_prs > 0:
        avg_score = sum(r.score for r in all_reviews) / total_prs
    else:
        avg_score = 0
    
    return {
        "total_prs_reviewed": total_prs,
        "total_bugs_found": total_bugs,
        "total_security_issues": total_security,
        "average_score": round(avg_score, 1)
    }