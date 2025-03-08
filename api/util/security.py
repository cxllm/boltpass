import hashlib
import requests


def check_password_leaked(password: str) -> int:
    """
    Check if a password has been leaked using the pwnedpasswords api

        Parameters:
            password (str): The password to check

        Returns:
            count (int): The number of leaks it was found in
    """
    # Encode the password using hashlib into sha1, and convert the hashed password to hex format
    # SHA1 is the method used by pwnedpasswords to hash their passwords
    password_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Request the pwnedpasswords API with the first 5 characters of the hash, this will return all hashes that have been leaked matching these first 5 characters
    response = requests.get(f"https://api.pwnedpasswords.com/range/{password_hash[:5]}")

    # if the response code is 200, it found matching hashes, so check if the one for this password matches any
    if response.status_code == 200:
        # split the format into hash digest and count of times leaked
        hashes = [line.split(":") for line in response.text.splitlines()]
        # linear search, check if our hash is included
        for hash_digest, count in hashes:
            # Use from 5 onwards as the first 5 are excluded (as they are in the search query)
            if password_hash[5:] == hash_digest:
                # Return the amount of times leaked
                return count

    # If it wasn't found then it can be assumed the password was leaked 0 times
    return 0


def check_instances_of_password(passwords: list[str]) -> dict[str, int]:
    """
    Check how many instances exist of a particular password in a set of data

        Parameters:
            passwords (list): A list of decrypted passwords

        Returns:
            counts (dict): A dictionary, keys are passwords, values are how many times they appear
    """
    counts = {}
    for decrypted in passwords:
        if decrypted in counts.keys():
            counts[decrypted] += 1
        else:
            counts[decrypted] = 0
    return counts
