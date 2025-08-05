# Visual Crypter 🖼🔐

Hide secret messages inside images using **AES-256 encryption** and retrieve them later.  
The project converts your encrypted text into a **PNG image**.

---

## 🚀 Features
- AES-256 CBC encryption with PBKDF2 key derivation
- Store encrypted data inside a PNG image
- Decrypt back to original text using password
- CLI tool with two commands: `encrypt` and `decrypt`
- Works with **direct message** or **text files**
- Includes padding validation (wrong password detection)

---

## 📂 Project Structure
```

visual-crypter/
├── pyproject.toml           # Package config
├── README.md
├── src/
│   └── visual\_crypter/
│       ├── **init**.py
│       ├── cli.py
│       ├── encryption.py
│       ├── image\_utils.py
└── tests/
    ├── test\_cli.py

````

---

## 🔧 Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/visual-crypter.git
cd visual-crypter

# Install in editable mode
pip install -e .
````

If you get `command not found` for `visualcrypter`, ensure `~/.local/bin` is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🛠 Usage

### Encrypt a message:

```bash
visualcrypter encrypt -m "Hello Secret World" -p "StrongPass"
# Output: encrypted.png
```

### Encrypt from file:

```bash
visualcrypter encrypt -f input.txt -p "StrongPass" -o secret.png
```

### Decrypt an image:

```bash
visualcrypter decrypt -i encrypted.png -p "StrongPass"
```

### Decrypt and save to file:

```bash
visualcrypter decrypt -i secret.png -p "StrongPass" -o output.txt
```

---

## ✅ CLI Options

### Encrypt:

```
visualcrypter encrypt [-m MESSAGE | -f FILE] -p PASSWORD [-o OUTPUT]
```

* `-m, --message`: Text to encrypt
* `-f, --file`: Text file with message
* `-p, --password`: Encryption password (required)
* `-o, --output`: Output image (default: encrypted.png)

### Decrypt:

```
visualcrypter decrypt -i INPUT -p PASSWORD [-o OUTPUT]
```

* `-i, --input`: Input image file
* `-p, --password`: Password for decryption
* `-o, --output`: Optional text file to save message

---

## 🧪 Running Tests

Install `pytest`:

```bash
pip install pytest
```

Run tests:

```bash
pytest -v
```

---

## 🛡 Security

* Uses AES-256 with PBKDF2 key derivation (100,000 iterations)
* Validates PKCS7 padding to detect wrong passwords
* Do NOT share your password. Losing it means data cannot be recovered.

---

## 📜 License

MIT License © 2025 Coskun Atak
