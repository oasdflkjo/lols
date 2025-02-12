import os
import subprocess
from datetime import datetime, timedelta

# Configurations
repo_name = "green-contribution-repo"
commit_message = "Automated commit"
file_name = "dummy.txt"
start_date = datetime.now() - timedelta(days=730)  # 2 years back

# Create a new Git repository
if not os.path.exists(repo_name):
    os.makedirs(repo_name)
    subprocess.run(["git", "init"], cwd=repo_name)

# Navigate to the repo
os.chdir(repo_name)

# Create a file to modify
if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("Starting commit history...\n")

# Loop through each day for 2 years
current_date = start_date
while current_date < datetime.now():
    for hour in range(24):  # 24 commits per day
        timestamp = current_date.replace(hour=hour, minute=0, second=0)
        formatted_time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")

        # Modify the file (so Git sees changes)
        with open(file_name, "a") as f:
            f.write(f"Commit at {formatted_time}\n")

        # Git commands
        subprocess.run(["git", "add", file_name])
        subprocess.run(["git", "commit", "-m", commit_message, "--date", formatted_time])

    # Move to the next day
    current_date += timedelta(days=1)

