import os
import io
import base64
import datetime
import pyotp
import qrcode


def generate_totp(name):

    random_bytes = os.urandom(20)  # generates a random sequences of bytes

    # Converts these bytes to base 32, then decode from a bytes object to a string
    secret_key = base64.b32encode(random_bytes).decode("utf-8")

    # create an instance of pyotp
    totp = pyotp.TOTP(secret_key)

    # generate a uri to enter into a qr code for scanning by apps such as authy or google auth
    uri = totp.provisioning_uri(name, issuer_name="BoltPass")
    print(uri)

    qr = qrcode.QRCode(
        version=1,  # size of qr code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used
        box_size=10,  # number of pixels in each box
        border=4,  # how many boxes thick the border should be
    )
    # add data to the qr code
    qr.add_data(uri)
    qr.make(fit=True)

    # generate the image with white background and boxes in white
    img = qr.make_image(fill="black", back_color="white")
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="PNG")
    img.show()
    byte_arr.seek(0)
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode("utf-8")
    encoded_img = encoded_img.replace("\n", "")
    return secret_key, encoded_img


def verify(secret_key, code):
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


def generate_code(secret_key):
    # create an instance of pyotp
    totp = pyotp.TOTP(secret_key)
    # get the current code
    code = totp.now()
    return code
