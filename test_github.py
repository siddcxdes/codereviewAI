from services.github_service import get_pr_files

repo = "siddcxdes/codereview-test"  
pr_number = 1  

files = get_pr_files(repo, pr_number)


print(f"\nTotal files found: {len(files)}")
for f in files:
    print(f"\n--- {f['filename']} ---")
    print(f['code'])