import subprocess
import sys


def get_changes():
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
        print("Current folder ins't Git.")
        sys.exit(1)
    except FileNotFoundError:
        print("Git isn't installed in your's computer.")
        sys.exit(1)

if __name__ == "__main__":
    print("Checking diff...")
    diff = get_changes()
    print("🎉 Успешно! Вот что пойдет в ИИ:\n")
    print(diff)
