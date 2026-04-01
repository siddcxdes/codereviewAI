def calculate_score(review_results):
    score = 100
    for file_result in review_results["results"]:
        agents = [
            file_result["bug_detection"],
            file_result["security_scan"],
            file_result["performance_check"],
            file_result["style_check"]
        ]
        
        for agent in agents:
            issues = agent.get("issues", [])
            for issue in issues:
                severity = issue.get("severity", "low")
                if severity == "high":
                    score = score - 8
                    
                elif severity == "medium":
                    score = score - 4
                    
                elif severity == "low":
                    score = score - 2
    if score < 0:
        score = 0

    if score >= 90:
        grade = "A"
        verdict = "Excellent! Ready to merge "
        
    elif score >= 75:
        grade = "B"
        verdict = "Good, minor issues to fix "
        
    elif score >= 60:
        grade = "C"
        verdict = "Needs some work before merging "
        
    elif score >= 40:
        grade = "D"
        verdict = "Significant issues found "
        
    else:
        grade = "F"
        verdict = "Critical issues! Do not merge "

    return {
        "total_score": score,
        "grade": grade,
        "verdict": verdict
    }