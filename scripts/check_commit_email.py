"""Check only new commits; report hashes without exposing author email values."""
import os
import re
import subprocess
import sys

SHA = re.compile(r"[0-9a-f]{40}\Z")


def private_email(email):
    value = email.casefold()
    return value.endswith("@users.noreply.github.com") or value == "noreply@github.com"


def main():
    head = os.getenv("HEAD_SHA", "HEAD")
    base = os.getenv("BASE_SHA", "")
    if head != "HEAD" and not SHA.fullmatch(head):
        raise SystemExit("Invalid head revision.")
    if base and not SHA.fullmatch(base):
        raise SystemExit("Invalid base revision.")
    revision = f"{base}..{head}" if base and set(base) != {"0"} else head
    command = ["git", "log", "--format=%H%x00%ae"]
    if not base or set(base) == {"0"}:
        command += ["-1"]
    output = subprocess.check_output(command + [revision], text=True)
    bad = []
    for line in output.splitlines():
        commit, email = line.split("\0", 1)
        if not private_email(email):
            bad.append(commit)
    if bad:
        print("New commits use a non-noreply email; see SECURITY.md.")
        for commit in bad:
            print(commit[:12])
        print("CI prevents merging; a commit already pushed may already expose its author email.")
        return 1
    print("Commit email privacy: checked new commits without printing addresses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
