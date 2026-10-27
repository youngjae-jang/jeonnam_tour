"""Reject tracked local secrets and generated files; never print file contents."""
from pathlib import PurePosixPath
import subprocess
import sys

GENERATED_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".hypothesis", ".venv", "venv", "htmlcov",
}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".keystore"}


def prohibited(path):
    parts = PurePosixPath(path).parts
    name = parts[-1]
    if any(part in GENERATED_DIRS for part in parts[:-1]):
        return True
    if name == ".env" or (name.startswith(".env.") and not name.endswith(".example")):
        return True
    if path == ".streamlit/secrets.toml" or name == "credentials.json":
        return True
    return (
        PurePosixPath(name).suffix.lower() in PRIVATE_SUFFIXES
        or name.endswith((".pyc", ".pyo", ".log"))
        or name == ".coverage" or name.startswith(".coverage.")
        or name in {"coverage.xml", ".DS_Store", "Thumbs.db"}
    )


def main():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    bad = [p for p in raw.decode("utf-8").split("\0") if p and prohibited(p)]
    if bad:
        print("Remove these local/generated files from Git tracking:")
        for path in bad:
            print(path)
        return 1
    print("Repository hygiene: no tracked local secrets or generated files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
