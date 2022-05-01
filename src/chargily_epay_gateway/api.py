
from django.http import HttpRequest

from .constants import BASE_CHARGILY_API, PAYMENT_ENDPOINT
from . import exceptions as ex
from .utils import get_api_key, get_secret_key
from .security import text2hash

import requests


def make_payment(**kwargs):
    payment_url = BASE_CHARGILY_API + PAYMENT_ENDPOINT
    headers = {
        "X-Authorization" : get_api_key(),
        "Accept" : 'application/json'
    }
    payloads = {
        'client':kwargs.get('client', None),
        'client_email':kwargs.get('client_email', None),
        'invoice_number':kwargs.get('invoice_number', None),
        'amount':kwargs.get('amount', None),
        'discount':kwargs.get('discount', None),
        'back_url':kwargs.get('back_url', None),
        'webhook_url':kwargs.get('webhook_url', None),
        'mode':kwargs.get('mode', None),
        'comment':kwargs.get('comment', None),
    }
    return requests.post(payment_url, headers=headers, data=payloads)


def webhook_is_valid(request: HttpRequest):
    """ Validate the sinature sent by Chargily """
    # Get Signature
    try:
        signature = request.headers['Signature']
    except KeyError:
        raise ex.ChargilyErrorSignatureMissing()
    # Hash the body
    confirm_signature = text2hash(request.body, get_secret_key())
    return signature == confirm_signature
