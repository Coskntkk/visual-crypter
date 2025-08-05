import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def derive_key(password: bytes, salt: bytes, iterations: int = 100000) -> bytes:
    """Derive a 256-bit AES key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password)


def encrypt_message(message: bytes, password: bytes) -> tuple:
    """Encrypt a message using AES-256 CBC and return salt, iv, ciphertext."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)

    # PKCS7 padding
    pad_len = 16 - (len(message) % 16)
    message_padded = message + bytes([pad_len] * pad_len)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message_padded) + encryptor.finalize()

    return salt, iv, ciphertext


def decrypt_message(salt: bytes, iv: bytes, ciphertext: bytes, password: bytes) -> str:
    """Decrypt AES-256 CBC encrypted data and validate PKCS7 padding."""
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()

    # Validate PKCS7 padding
    pad_len = padded_message[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Incorrect password or corrupted data (invalid padding).")
    if padded_message[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Incorrect password or corrupted data (invalid padding pattern).")

    message = padded_message[:-pad_len]
    return message.decode('utf-8')
