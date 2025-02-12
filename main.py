import os
import subprocess
from datetime import datetime, timedelta

# Configurations
repo_name = "green-contribution-repo"
file_name = "dummy.txt"
commit_message = "Automated commit"
start_date = datetime.now() - timedelta(days=730)  # 2 years back
github_repo = "git@github.com:oasdflkjo/green-contribution-repo.git"  # Change this!

# Step 1: Create and initialize repo if not exists
if not os.path.exists(repo_name):
    os.makedirs(repo_name)
    subprocess.run(["git", "init"], cwd=repo_name)
    subprocess.run(["git", "config", "user.name", "REPLACE_WITH_YOUR_NAME"], cwd=repo_name)
    subprocess.run(["git", "config", "user.email", "REPLACE_WITH_YOUR_EMAIL"], cwd=repo_name)

os.chdir(repo_name)

# Generate commit timestamps
commit_dates = []
current_date = start_date
while current_date < datetime.now():
    for hour in range(24):  # 24 commits per day
        timestamp = current_date.replace(hour=hour, minute=0, second=0)
        commit_dates.append(timestamp)
    current_date += timedelta(days=1)

# Use git fast-import for bulk importing
print(f"Creating {len(commit_dates)} commits...")
git_import = subprocess.Popen(['git', 'fast-import'], stdin=subprocess.PIPE)

# Create the first commit with an empty file
content = "Starting commit history...\n"
git_import.stdin.write(f"""blob
mark :1
data {len(content)}
{content}
commit refs/heads/master
mark :2
author oasdflkjo <petri.pihla@gmail.com> {int(commit_dates[0].timestamp())} +0000
committer oasdflkjo <petri.pihla@gmail.com> {int(commit_dates[0].timestamp())} +0000
data {len(commit_message)}
{commit_message}
M 100644 :1 {file_name}
""".encode())

# Create subsequent commits
for i, commit_date in enumerate(commit_dates[1:], start=1):
    mark_blob = i * 2 + 1
    mark_commit = mark_blob + 1
    prev_commit = mark_blob - 1
    content = f"Commit {i} at {commit_date.isoformat()}\n"
    
    command = f"""blob
mark :{mark_blob}
data {len(content)}
{content}
commit refs/heads/master
mark :{mark_commit}
author oasdflkjo <petri.pihla@gmail.com> {int(commit_date.timestamp())} +0000
committer oasdflkjo <petri.pihla@gmail.com> {int(commit_date.timestamp())} +0000
data {len(commit_message)}
{commit_message}
from :{prev_commit}
M 100644 :{mark_blob} {file_name}
""".encode()
    
    try:
        git_import.stdin.write(command)
    except OSError as e:
        print(f"Error at commit {i}: {e}")
        break
    
    if i % 1000 == 0:  # Progress indicator every 1000 commits
        print(f"Progress: {i}/{len(commit_dates)} commits created")

git_import.stdin.close()
git_import.wait()

print("✅ All commits created successfully!")
