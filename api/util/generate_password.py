import string
import secrets
import random

MAX_LENGTH = 200


class LengthTooHighError(Exception):
    # error for when the length requested is too long
    pass


class LengthTooLowError(Exception):
    # error for when the length requests is too short
    pass


def password_generator(
    length=20, incl_uppercase=True, incl_numbers=True, incl_special_chars=True
):
    """
    Generates a random secure password

        Paramaters:
            length (int): The length of the generated password (default 20)
            incl_uppercase (bool): Whether or not to include uppercase characters (default True)
            incl_numbers (bool): Whether or not to include numbers (default True)
            incl_special_chars (bool): Whether or not to include special characters (default True)

        Returns:
            password (string): The generated password based on the inputted paramaters
    """
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase if incl_uppercase else ""
    digits = string.digits if incl_numbers else ""
    special_chars = "!@#$%^&*" if incl_special_chars else ""

    # characters that you should select from
    all_characters = lowercase_letters + uppercase_letters + digits + special_chars
    mandatory = (  # ensures all the characters you need are in the password
        (secrets.choice(uppercase_letters) if incl_uppercase else "")
        + (secrets.choice(lowercase_letters))
        + (secrets.choice(digits) if incl_numbers else "")
        + (secrets.choice(special_chars) if incl_special_chars else "")
    )
    # if the password is not long enough (lower than the amount of mandatory characters)
    if len(mandatory) > length:
        raise LengthTooLowError
    # if the password requested is too long
    elif length > MAX_LENGTH:
        raise LengthTooHighError

    # generate a random password
    password = "".join(
        secrets.choice(all_characters) for _ in range(length - len(mandatory))
    )
    for char in mandatory:
        # insert the mandatory characters in random places so the password remains secure
        index = random.randint(0, length - len(mandatory))
        password = password[0:index] + char + password[index:]

    return password


# only run this if the file is being called directly and not imported (only for testing purposes)
if __name__ == "__main__":
    print(password_generator())
