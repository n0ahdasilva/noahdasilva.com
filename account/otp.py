import re
import pyotp
import qrcode
from qrcode.image.svg import SvgImage
from io import BytesIO

class OTP():
    def generate_secret():
        return pyotp.random_base32()

    def generate_qrcode(name, secret):
        stream = BytesIO()
        img = qrcode.make(pyotp.totp.TOTP(secret).provisioning_uri(name=name, issuer_name='noahdasilva.com'), image_factory=SvgImage)
        img.save(stream)
        return stream.getvalue().decode()

    def verify_otp(otp_secret, otp):
        totp = pyotp.TOTP(otp_secret)
        return totp.verify(otp)