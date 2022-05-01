
from django.conf import settings

from . import exceptions as ex


def get_api_key():
    try:
        api_key = settings.CHARGILY_API_KEY
    except AttributeError:
        raise ex.ChargilyErrorAPIMissing('CHARGILY_API_KEY')
    return api_key


def get_secret_key():
    try:
        secret_key = settings.CHARGILY_SECRET_KEY
    except AttributeError:
        raise ex.ChargilyErrorAPIMissing('CHARGILY_SECRET_KEY')
    return secret_key
