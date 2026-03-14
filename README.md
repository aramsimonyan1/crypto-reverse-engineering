# Breaking a Flawed Diffie-Hellman Implementation (Python Reverse Engineering)

## Project Overview

This project demonstrates the reverse engineering and cryptanalysis of a Python application implementing a vulnerable Diffie-Hellman key exchange.

The challenge involved analysing a suspicious executable and intercepted communication between two parties. By reverse engineering the application and identifying a cryptographic implementation flaw, it was possible to recover the shared secret and decrypt the protected message.

The project highlights how implementation mistakes in cryptographic protocols can completely compromise security, even when strong algorithms such as Diffie-Hellman and AES are used.

## Challenge Scenario

At the beginning of the challenge, a ZIP archive was provided containing:

A text file with a short intercepted communication between two users (Alice and Bob).

A file without a visible extension, which turned out to be a compiled executable.

The intercepted conversation revealed that Alice encrypted a flag before sending it to Bob using their custom Python implementation of Diffie-Hellman.

Example excerpt from the intercepted communication:

Alice: Hey, I managed to get another flag from H@ckademy
Bob: Oh, send it please
Alice: Sure, but just in case I'll encrypt it. Who knows who might be listening.
Bob: OK
Alice: Let's use our reliable Diffie-Hellman program.

The communication also included the following parameters:
Prime modulus p
Public key A (Alice)
Public key B (Bob)
Base64-encoded ciphertext

### Challenge Objective

The task was to:
Analyse the provided executable.
Understand how the key exchange and encryption were implemented.
Identify any weaknesses in the cryptographic protocol.
Recover the shared secret used between Alice and Bob.
Use the secret to derive the AES key and decrypt the encrypted message (the flag).

### Methodology
1. Extracting the PyInstaller executable
The provided binary was identified as a PyInstaller-packed Python application.
Using pyinstxtractor, the contents of the executable were extracted:
    python pyinstxtractor.py dh_secret.exe
This revealed multiple files including:
Python runtime libraries
bundled dependencies
a compiled Python bytecode file:
    DH shared secret generation.pyc

2. Recovering the Python source code
The .pyc file was decompiled into readable Python code using an online decompiler:
    https://pychaos.io

This allowed analysis of the program logic responsible for:
Diffie-Hellman key exchange
AES encryption/decryption

3. Identifying the cryptographic flaw
During analysis, a critical implementation error was discovered.

The program used the following code to generate Diffie-Hellman values:
    def generate_public_int(g,a,p):
        return g^a%p
However, in Python the operator ^ represents bitwise XOR, not exponentiation.

Correct Diffie-Hellman should use modular exponentiation:
    pow(g, a, p)

Instead, the program effectively computed:
    A = g XOR (a mod p)
This mistake completely breaks the security of the key exchange.

### 4. Reconstructing protocol parameters
The generator value g was derived from a hardcoded string in the source code:
    g = int(licenseText[39] + licenseText[89])

By evaluating these indices, the generator was determined to be:
    g = 11

### 5. Recovering the shared secret

Because XOR was used instead of exponentiation, the public keys reveal the private values directly.

Given:
    B = g ^ (b % p)

we can recover:
    b % p = g ^ B

The shared secret used by the program was then calculated as:
    shared_secret = A ^ (b % p)

This allowed reconstruction of the exact secret used during encryption.

### 6. Decrypting the message
The program derived the AES key using:
```bash    
AES_key = SHA256(shared_secret)
```

Encryption mode:
```bash
AES-CBC
```
Using the recovered secret, the ciphertext was successfully decrypted.

### Result
Recovered flag:
```bash
KPMG{Have_you-eva-s33n_binary_python?}
```

### Key Lessons
This challenge demonstrates several important cybersecurity concepts:
- Reverse engineering PyInstaller executables
- Python bytecode analysis
- Cryptographic protocol analysis
- The dangers of incorrect cryptographic implementations
- How small coding mistakes can completely break security guarantees
- Even though the program attempted to use strong cryptographic primitives (Diffie-Hellman and AES), the misuse of the XOR operator instead of exponentiation made the protocol trivially exploitable.

### Tools Used
- Python
- pyinstxtractor
- Python bytecode decompilers
- PyCryptodome
- Base64 decoding
- Cryptographic analysis