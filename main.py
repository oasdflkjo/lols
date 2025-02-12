import os
import subprocess
from datetime import datetime, timedelta

# Configurations
repo_name = "green-contribution-repo"
file_name = "dummy.txt"
commit_message = "Automated commit"
start_date = datetime.now() - timedelta(days=730)  # 2 years back
github_repo = "git@github.com:YOUR_USERNAME/green-contribution-repo.git"  # Change this!

# Create and initialize the repo if not exists
if not os.path.exists(repo_name):
    os.makedirs(repo_name)
    subprocess.run(["git", "init"], cwd=repo_name)

os.chdir(repo_name)

# Ensure the file exists
if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("Starting commit history...\n")

# Create a branch if needed
subprocess.run(["git", "checkout", "-B", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Store commit timestamps to batch process them
commit_dates = []
current_date = start_date

while current_date < datetime.now():
    for hour in range(24):  # 24 commits per day
        timestamp = current_date.replace(hour=hour, minute=0, second=0)
        commit_dates.append(timestamp.strftime("%Y-%m-%dT%H:%M:%S"))
    current_date += timedelta(days=1)

# Commit in bulk using git commit-tree for MAX SPEED 🚀
for i, commit_time in enumerate(commit_dates):
    with open(file_name, "a") as f:
        f.write(f"Commit {i} at {commit_time}\n")

    subprocess.run(["git", "add", file_name])
    tree_hash = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
    parent_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    commit_args = ["git", "commit-tree", tree_hash, "-m", commit_message, "--date", commit_time]
    
    if parent_commit:
        commit_args.insert(-1, "-p")
        commit_args.insert(-1, parent_commit)
    
    commit_hash = subprocess.run(commit_args, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "update-ref", "HEAD", commit_hash])
