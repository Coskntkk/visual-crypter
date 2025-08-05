import math
from PIL import Image


def create_image_from_data(salt: bytes, iv: bytes, ciphertext: bytes, output_path: str):
    """Create an image from encrypted data."""
    cipher_length = len(ciphertext)
    header = salt + iv + cipher_length.to_bytes(4, 'big')
    full_data = header + ciphertext

    # Calculate square image size
    pixel_count = math.ceil(len(full_data) / 3)
    size = math.ceil(math.sqrt(pixel_count))

    # Pad to fit full pixels
    full_data += b'\x00' * (size * size * 3 - len(full_data))

    # Convert to RGB
    pixels = []
    for i in range(0, len(full_data), 3):
        r, g, b = full_data[i:i+3]
        pixels.append((r, g, b))

    img = Image.new('RGB', (size, size))
    img.putdata(pixels)
    img.save(output_path)
    return size


def extract_data_from_image(image_path: str):
    """Extract salt, iv, ciphertext length, and ciphertext from image."""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Convert to bytes
    data = bytearray()
    for r, g, b in pixels:
        data.extend([r, g, b])

    salt = bytes(data[0:16])
    iv = bytes(data[16:32])
    cipher_length = int.from_bytes(data[32:36], 'big')
    ciphertext = bytes(data[36:36 + cipher_length])
    return salt, iv, ciphertext
