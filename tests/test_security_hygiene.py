"""Meaningful boundaries for local-only files and author email privacy."""
import importlib.util
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gitignore_blocks_secrets_and_keeps_empty_examples(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text((ROOT / ".gitignore").read_text())
    for path in [".env", ".env.production", ".streamlit/secrets.toml", "key.pem", "key.key", "nested/__pycache__/a.pyc", ".coverage", ".pytest_cache/a"]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=tmp_path)
        assert result.returncode == 0, path
    for path in [".env.example", ".env.production.example", ".streamlit/secrets.toml.example", "config.py", "data/jeonnam.csv"]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=tmp_path)
        assert result.returncode == 1, path


def test_hygiene_guard_checks_tracked_files_even_when_ignore_was_bypassed(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".env").write_text("EXAMPLE=placeholder")
    subprocess.run(["git", "add", "-f", ".env"], cwd=tmp_path, check=True)
    import sys
    result = subprocess.run([sys.executable, str(ROOT / "scripts/check_repository_hygiene.py")], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 1
    assert ".env" in result.stdout
    assert "placeholder" not in result.stdout + result.stderr


def test_email_policy_rejects_personal_and_lookalike_domains():
    guard = load_script("check_commit_email")
    assert guard.private_email("123+example@users.noreply.github.com")
    assert guard.private_email("noreply@github.com")
    assert not guard.private_email("example@example.com")
    assert not guard.private_email("example@users.noreply.github.com.example.com")
    assert not guard.private_email("")
