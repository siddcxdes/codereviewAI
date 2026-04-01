import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_pr_files(repo_name: str, pr_number: int):
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f" Error fetching PR files: {response.status_code}")
        print(f"   Message: {response.text}")
        return []
    
    files = response.json()

    changed_files = []
    
    for file in files:
        filename = file.get("filename", "")

        patch = file.get("patch", "")
        if not patch:
            continue
        
        changed_files.append({
            "filename": filename,
            "code": patch
        })
        
        print(f"Found changed file: {filename}")

    return changed_files


def post_pr_comment(repo_name: str, pr_number: int, comment: str):
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"

    data = {
        "body": comment
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 201:
        print(f"Comment posted successfully on PR #{pr_number}")
    else:
        print(f"Failed to post comment: {response.status_code}")
        print(f"   Message: {response.text}")