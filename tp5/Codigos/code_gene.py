#!/usr/bin/env python3
# code_gene.py

"""
Generates a Fernet (symmetric encryption) key.

This script is a utility to create a new, cryptographically strong key
suitable for use with the Fernet symmetric encryption scheme. The generated
key should be securely shared between the client and server applications
that need to encrypt and decrypt messages.
"""

from cryptography.fernet import Fernet

def generate_and_print_key() -> None:
    """
    Generates a Fernet key and prints it to the console.
    The output key is a base64-encoded string, which should be copied
    and pasted into the ENCRYPTION_KEY variable in the configuration files
    (e.g., config_client.py, config_server.py).
    """
    key: bytes = Fernet.generate_key()
    print("Generated Fernet key (copy this value):")
    print(key.decode()) # Decode to string for easy copying

if __name__ == "__main__":
    # This script is intended to be run directly to generate a key.
    generate_and_print_key()
