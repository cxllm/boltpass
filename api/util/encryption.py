import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7


def derive_key(
    password: str, salt: str, iterations: int = 100000, key_length: int = 32
) -> tuple[bytes, hex]:
    """
    Derives a cryptographic key from a password using PBKDF2.

        Parameters:
            password (str): The password to derive from
            salt (str): The salt to use to derive the key
            iterations (int): Number of iterations to use (default 100,000)
            key_length (int): How long the key should be in bytes
        Returns:
            key (bytes): The key in bytes form
            key (str): The key in hexadecimal form
    """
    kdf = PBKDF2HMAC(
        # using a different type of hashing to avoid clashes
        algorithm=hashes.MD5(),
        length=key_length,
        salt=bytes.fromhex(salt),
        iterations=iterations,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode())
    return key, key.hex()


def encrypt(data: str, key: str) -> tuple[str]:
    """
    Encrypts the given data using AES with a PBKDF2-derived key.
        Parameters:
            data (str): Data to encrypt
            key (str): Key to use for encryption
        Returns:
            ciphertext (str): The encrypted data
            salt (str): The salt used
            iv (str): The initialisation vector used
    """
    # Generate a random salt and IV
    salt = os.urandom(
        16
    )  # uses a different salt to the master password and needs to be stored alongside the password
    iv = os.urandom(
        16
    )  # store this alongside the encrypted password as well, adds randomness to the encryption process.
    # salt and IV prevent the same password from producing the same output

    # Encode key
    key = bytes.fromhex(key)

    # Pad data to match AES block size (128-bit)
    # PKCS7 is a method used to pad data to the size needed by adding extra bytes at the end
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Encode as Hex for storage/transmission
    return (ciphertext.hex(), salt.hex(), iv.hex())


def decrypt(ciphertext: str, salt: str, iv: str, key: str) -> str:
    """
    Decrypts data using AES with a PBKDF2-derived key.
        Parameters:
            ciphertext (str): The encrypted data
            salt (str): The salt used
            iv (str): The initialisation vector used
            key (str): Key to use for encryption
        Returns:
            data (str): The decoded data

    """
    # Decode Base64-encoded components
    ciphertext = bytes.fromhex(ciphertext)
    salt = bytes.fromhex(salt)
    iv = bytes.fromhex(iv)
    # use the same salt and IV

    # Encode key
    key = bytes.fromhex(key)

    # Decrypt data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data.decode()


if __name__ == "__main__":
    key = derive_key("Hello123!", "bd5ce17990eae13c678ef9e28eca8e25")
    print(key, key[1], bytes.fromhex(key[1]) == key[0])
    print(encrypt("hello", key[1]))
    print(
        decrypt(
            "656f5f27445bee497635036cf04b8dc2",
            "35c9c7e25b37e115051e15e4e0485f22",
            "31b32dde3f0fe697799085dc37e0eda6",
            key[1],
        )
    )
