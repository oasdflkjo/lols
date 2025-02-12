import os
import subprocess
from datetime import datetime, timedelta

# Configurations
repo_name = "green-contribution-repo"
file_name = "dummy.txt"
commit_message = "Automated commit"
start_date = datetime.now() - timedelta(days=730)  # 2 years back
github_repo = "git@github.com:YOUR_USERNAME/green-contribution-repo.git"  # Change this!

# Step 1: Create Repo if not exists
if not os.path.exists(repo_name):
    os.makedirs(repo_name)
    subprocess.run(["git", "init"], cwd=repo_name)

# Navigate to repo
os.chdir(repo_name)

# Ensure the file exists
if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("Starting commit history...\n")

# Step 2: Fast commit generation
current_date = start_date
commit_data = []  # Store all commit timestamps to reduce shell calls

while current_date < datetime.now():
    for hour in range(24):  # 24 commits per day
        timestamp = current_date.replace(hour=hour, minute=0, second=0)
        formatted_time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        commit_data.append(formatted_time)
    current_date += timedelta(days=1)

# Step 3: Create all commits in bulk
for i, commit_time in enumerate(commit_data):
    with open(file_name, "a") as f:
        f.write(f"Commit {i} at {commit_time}\n")

    subprocess.run(["git", "add", file_name])
    subprocess.run(["git", "commit", "-m", commit_message, "--date", commit_time], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
