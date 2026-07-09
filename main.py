import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from config import SYSTEM_PROMPT, CommitMessage
from spinner import CLISpinner

load_dotenv()

def get_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            encoding="utf-8",
            check=True
        )

        diff_text = result.stdout.strip()

        if not diff_text:
            print("No files in stage. Do 'git add .'")
            sys.exit(0)

        return diff_text

    except subprocess.CalledProcessError:
        print("Current folder isn't Git.")
        sys.exit(1)
    except FileNotFoundError:
        print("Git isn't installed on your computer.")
        sys.exit(1)

def generate_commit(diff: str) -> CommitMessage:
    provider = GoogleProvider(api_key= os.environ['GEMINI_API_KEY'])

    model = GoogleModel(
        model_name='gemini-3.1-flash-lite',
        provider=provider
    )

    commiter = Agent(
        model=model,
        deps_type=str,
        output_type=CommitMessage,
        system_prompt=SYSTEM_PROMPT
    )

    try:
        result = commiter.run_sync(deps=diff)
        return result.output
    except Exception as e:
        print(f"Failed to process or validate output: {e}")
        sys.exit(1)

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="AI Git Commiter")
    parser.add_argument("--emoji", action="store_true", help="Add gitmoji to the message")
    args = parser.parse_args()

    diff = get_diff()

    with CLISpinner("Processing diff..."):
        commit_data = generate_commit(diff)

    commit_string = commit_data.to_string(use_emoji=args.emoji)
    print(f"Generated commit: {commit_string}")

    try:
        subprocess.run(["git", "commit", "-m", commit_string], check=True, capture_output=True)
        print("Successfully committed to repository!")
    except subprocess.CalledProcessError:
        print("Failed to execute git commit command.")
