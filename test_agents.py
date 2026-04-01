# This tests that our agents can analyze real PR code
from services.github_service import get_pr_files
from services.review_service import run_full_review

# Your repo and PR number
repo = "siddcxdes/codereview-test"  # ← your GitHub username
pr_number = 1  

# Step 1: Get the real code from GitHub
print("Fetching PR files from GitHub...")
files = get_pr_files(repo, pr_number)

# Step 2: Run all agents on the code
review = run_full_review(files)

# Step 3: Print the results nicely
print("\n" + "="*50)
print("FULL REVIEW RESULTS")
print("="*50)

# Loop through each file's results
for file_result in review["results"]:
    print(f"\nFile: {file_result['filename']}")
    print("-"*40)
    
    # Print each agent's findings
    for agent_key in ["bug_detection", "security_scan", "performance_check", "style_check"]:
        agent_result = file_result[agent_key]
        print(f"\n{agent_result.get('agent', agent_key)}:")
        print(f"   Summary: {agent_result.get('summary', 'N/A')}")
        
        # Print each issue found
        issues = agent_result.get("issues", [])
        if issues:
            for issue in issues:
                severity = issue.get('severity', 'unknown').upper()
                problem = issue.get('problem', 'N/A')
                fix = issue.get('fix', 'N/A')
                print(f"   [{severity}] {problem}")
                print(f" Fix: {fix}")
        else:
            print("No issues found!")