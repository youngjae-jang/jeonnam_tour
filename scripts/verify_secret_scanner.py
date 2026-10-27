"""Verify the real scanner detects synthetic Kakao values and redacts output."""
from pathlib import Path
import subprocess
import sys
import tempfile

scanner = str(Path(sys.argv[1]).resolve())
config = str(Path(__file__).resolve().parents[1] / ".gitleaks.toml")
# Construct test-only values at runtime so fixtures never resemble stored keys.
value = "".join(format(i % 16, "x") for i in range(32))
with tempfile.TemporaryDirectory() as directory:
    target = Path(directory) / "fixture.txt"
    for fixture in ("KAKAO_REST_API_KEY = \"" + value + "\"", "Authorization: KakaoAK " + value):
        target.write_text(fixture, encoding="utf-8")
        result = subprocess.run(
            [scanner, "dir", directory, "--config", config, "--redact=100", "--no-banner", "--no-color"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 1 or value in result.stdout + result.stderr:
            raise SystemExit("Secret-scanner detection/redaction self-test failed.")
    target.write_text('KAKAO_REST_API_KEY = ""', encoding="utf-8")
    result = subprocess.run(
        [scanner, "dir", directory, "--config", config, "--redact=100", "--no-banner", "--no-color"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Secret-scanner empty-placeholder self-test failed.")
print("Secret scanner self-test: synthetic credentials detected, output redacted, empty example allowed.")
