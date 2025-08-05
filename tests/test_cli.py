import subprocess
import os
import tempfile
import shutil
import pytest

CLI_CMD = ["visualcrypter"]

@pytest.fixture
def temp_dir():
    """Create and clean up a temporary directory for tests."""
    d = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(d)
    yield d
    os.chdir(cwd)
    shutil.rmtree(d)

def run_cli(args):
    """Run CLI command and return (stdout, stderr, exit_code)."""
    result = subprocess.run(CLI_CMD + args, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def test_encrypt_and_decrypt_message(temp_dir):
    """Encrypt a message and then decrypt it."""
    message = "Hello Visual Crypter!"
    password = "StrongPass123"

    # Encrypt
    stdout, stderr, code = run_cli(["encrypt", "-m", message, "-p", password])
    assert code == 0
    assert "Encrypted image created" in stdout
    assert os.path.exists("encrypted.png")

    # Decrypt
    stdout, stderr, code = run_cli(["decrypt", "-i", "encrypted.png", "-p", password])
    assert code == 0
    assert message in stdout

def test_encrypt_from_file(temp_dir):
    """Encrypt text from a file and decrypt it."""
    text_file = "input.txt"
    message = "Secret from file"
    password = "FilePass123"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(message)

    # Encrypt
    stdout, stderr, code = run_cli(["encrypt", "-f", text_file, "-p", password, "-o", "file_enc.png"])
    assert code == 0
    assert os.path.exists("file_enc.png")

    # Decrypt to file
    stdout, stderr, code = run_cli(["decrypt", "-i", "file_enc.png", "-p", password, "-o", "output.txt"])
    assert code == 0
    with open("output.txt", "r", encoding="utf-8") as f:
        decrypted = f.read()
    assert decrypted == message

def test_wrong_password(temp_dir):
    """Decrypt with wrong password should fail."""
    message = "Wrong password test"
    password = "CorrectPass"

    # Encrypt first
    run_cli(["encrypt", "-m", message, "-p", password])

    # Attempt decrypt with wrong password
    stdout, stderr, code = run_cli(["decrypt", "-i", "encrypted.png", "-p", "WrongPass"])
    assert code != 0
    assert "Incorrect password" in stdout or "Decryption failed" in stdout
