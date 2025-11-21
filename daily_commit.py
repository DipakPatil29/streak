import os
import datetime

# --- Configuration ---
# File to modify and commit. Must be tracked by Git.
COMMIT_FILE = "last_contribution.txt" 
REPO_NAME = "My Daily Contrib Repo" # Use your actual repository name
# --- Configuration ---


def update_contribution_file():
    """Updates the timestamp in the file, ensuring a change is made."""
    print(f"1. Updating the file: {COMMIT_FILE}")
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"Last automatic contribution made on: {now}\n\nThis file is updated daily by a scheduled GitHub Action to maintain a contribution streak."

        with open(COMMIT_FILE, "w") as f:
            f.write(content)
        
        print(f"   Successfully updated {COMMIT_FILE}.")
        return True
    except IOError as e:
        print(f"Error updating file: {e}")
        return False

def run_git_commands():
    """Executes the necessary Git commands to stage, commit, and push."""
    print("2. Running Git commands...")
    try:
        # Check if there are changes to commit (important if the script is run manually)
        if os.system(f"git diff --exit-code --quiet {COMMIT_FILE}") != 0:
            
            # Stage the changes
            os.system(f"git add {COMMIT_FILE}")
            print("   -> Staged changes.")

            # Commit the changes
            commit_message = f"🤖 Daily Contribution: {datetime.date.today()} - Auto-commit for streak maintenance."
            os.system(f'git commit -m "{commit_message}"')
            print(f"   -> Committed with message: {commit_message}")

            # Push the changes to the remote repository
            # In GitHub Actions, 'main' or 'master' is usually the default branch.
            # We use 'origin HEAD' to push to the current branch the action is running on.
            if os.system("git push origin HEAD") == 0:
                print(f"3. Success! Changes pushed to {REPO_NAME}.")
                return True
            else:
                print("Error: Git push failed.")
                return False
        else:
            print("No change detected in the file. Skipping commit/push.")
            return True

    except Exception as e:
        print(f"An error occurred during Git operations: {e}")
        return False

if __name__ == "__main__":
    if update_contribution_file():
        run_git_commands()
