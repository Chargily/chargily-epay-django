import hmac
import hashlib
import base64


def text2hash(message, secret_key):
    if not isinstance(secret_key, bytes):
        secret_key = bytes(secret_key, 'utf-8')
    if not isinstance(message, bytes):
        message = bytes(message, 'utf-8')
    dig = hmac.new(secret_key, msg=message, digestmod=hashlib.sha256)
    return dig.hexdigest()

# TODO: implemenet hash for pyhon 2.7
