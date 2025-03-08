import os
import io
import string
import random
import base64
import datetime
import pyotp
import qrcode


def generate_recovery_codes(codes_to_generate: int = 8, length: int = 8):
    """
    Generates a random string of recovery codes

        Parameters:
            codes_to_generate (int): The number of codes to generate
            length (int): How long you want the codes to be

        Returns:
            codes (list): The generated recovery codes
    """
    alphabet = string.ascii_lowercase + string.digits  # the alphabet to use
    codes = []
    # generate all of the codes randomly
    for _ in range(codes_to_generate):
        code = ""
        for _ in range(length):
            code += random.choice(alphabet)
        codes.append(code)
    return codes


def generate_totp(name):
    """
    Generates a random TOTP combination

        Parameters:
            name (str): The name to be attributed to the QR code

        Returns:
            secret_key (str): The secret for the TOTP config
            encoded_img (str): The QR code data encoded in base 64
    """

    random_bytes = os.urandom(20)  # generates a random sequences of bytes

    # Converts these bytes to base 32, then decode from a bytes object to a string
    secret_key = base64.b32encode(random_bytes).decode("utf-8")

    # create an instance of pyotp
    totp = pyotp.TOTP(secret_key)

    # generate a uri to enter into a qr code for scanning by apps such as authy or google auth
    uri = totp.provisioning_uri(name, issuer_name="BoltPass")

    qr = qrcode.QRCode(
        version=1,  # size of qr code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used
        box_size=10,  # number of pixels in each box
        border=1,  # how many boxes thick the border should be
    )
    # add data to the qr code
    qr.add_data(uri)
    qr.make(fit=True)

    # generate the image with white background and boxes in white
    img = qr.make_image(fill="black", back_color="white")

    # convert the image to bytes
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    # convert this to base64 and get rid of line breaks
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode("utf-8")
    encoded_img = encoded_img.replace("\n", "")
    return secret_key, encoded_img, generate_recovery_codes()


def verify(secret_key, code):
    """
    Verifies a code against a TOTP secret for right now or 30 seconds ago

        Parameters:
            secret_key (str): The secret for the TOTP config
            code (str): The code to verify

        Returns:
            output (bool): Whether the key is valid or not
    """
    # create an instance of pyotp
    totp = pyotp.TOTP(secret_key)
    # Checks if code is valid now or was valid 30 seconds ago
    if totp.verify(code) is True:
        return True
    else:
        thirty_seconds_ago = datetime.datetime.fromtimestamp(
            datetime.datetime.now().timestamp() - 30
        )
        return totp.verify(code, for_time=thirty_seconds_ago)


def generate_code(secret_key: str) -> str:
    """
    Generates a code for a TOTP secret for right now

        Parameters:
            secret_key (str): The secret for the TOTP config

        Returns:
            code (bool): The code for right now
    """
    # create an instance of pyotp
    totp = pyotp.TOTP(secret_key)
    # get the current code
    code = totp.now()
    return code
