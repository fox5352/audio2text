"""Audio processing test script with PEP 8 compliance."""
import sys
import base64
import subprocess
from pathlib import Path


# Use venv Python interpreter
if sys.platform != "win32":
    venv_python = Path("venv/bin/python")
else:
    venv_python = Path("venv/Scripts/python.exe")

# Load audio file
try:
    with open("./assets/test.mp3", "rb") as f:
        audio_data = f.read()
except FileNotFoundError:
    print("Missing test file: ./assets/test.mp3", file=sys.stderr)
    sys.exit(1)


def process(cmd, input_text=None):
    """Run subprocess command and return result."""
    return subprocess.run(
        cmd,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False
    )


def test_without_audio_buffer():
    """Test script behavior with empty audio buffer."""
    print("Running test_without_audio_buffer...")
    cmd = [str(venv_python), "main.py", "-a", ""]
    result = process(cmd)
    print("STDERR:", result.stderr.strip())
    print("RETURN CODE:", result.returncode)
    
    expected_msg = "Expected non-zero exit code for empty audio buffer"
    assert result.returncode != 0, expected_msg


def test_with_audio_buffer():
    """Test script behavior with valid audio buffer."""
    print("Running test_with_audio_buffer...")
    encoded = base64.b64encode(audio_data).decode("utf-8")
    cmd = [str(venv_python), "main.py", "-a", "-"]
    result = process(cmd, input_text=encoded)
    print("STDOUT:", result.stdout.strip())
    print("STDERR:", result.stderr.strip())
    print("RETURN CODE:", result.returncode)
    
    expected_msg = "Expected successful exit with valid audio buffer"
    assert result.returncode == 0, expected_msg
    assert "decoded successfully" in result.stdout.lower()


if __name__ == "__main__":
    test_without_audio_buffer()
    test_with_audio_buffer()