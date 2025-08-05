import argparse
import sys
from visual_crypter.encryption import encrypt_message, decrypt_message
from visual_crypter.image_utils import create_image_from_data, extract_data_from_image


def encrypt_command(args):
    if args.message:
        message = args.message.encode('utf-8')
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                message = f.read().encode('utf-8')
        except FileNotFoundError:
            print("Error: Input file not found.")
            sys.exit(1)
    else:
        print("Error: Provide a message (-m) or a text file (-f).")
        sys.exit(1)

    salt, iv, ciphertext = encrypt_message(message, args.password.encode('utf-8'))
    size = create_image_from_data(salt, iv, ciphertext, args.output)
    print(f"✅ Encrypted image created: {args.output} ({size}x{size})")


def decrypt_command(args):
    try:
        salt, iv, ciphertext = extract_data_from_image(args.input)
        message = decrypt_message(salt, iv, ciphertext, args.password.encode('utf-8'))
    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(message)
        print(f"✅ Message saved to: {args.output}")
    else:
        print("\n✅ Original Message:")
        print(message)


def main():
    parser = argparse.ArgumentParser(description="Visual Crypter: Hide text inside images using AES encryption.")
    subparsers = parser.add_subparsers(title="commands", description="Available operations")

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help="Encrypt a message and generate an image.")
    group = encrypt_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--message", help="Message to encrypt")
    group.add_argument("-f", "--file", help="Text file containing the message")
    encrypt_parser.add_argument("-p", "--password", required=True, help="Password for encryption")
    encrypt_parser.add_argument("-o", "--output", default="encrypted.png", help="Output image file name (default: encrypted.png)")
    encrypt_parser.set_defaults(func=encrypt_command)

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help="Decrypt an image to reveal the original message.")
    decrypt_parser.add_argument("-i", "--input", required=True, help="Input image file")
    decrypt_parser.add_argument("-p", "--password", required=True, help="Password for decryption")
    decrypt_parser.add_argument("-o", "--output", help="Output text file (optional)")
    decrypt_parser.set_defaults(func=decrypt_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
