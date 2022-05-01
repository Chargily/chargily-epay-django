import os
import json

import requests


EPAY_MODE_OPTIONS = ["EDAHABIA", "CIB"]

REQUES_TYPE = "POST"

REQUES_URL = "https://epay.chargily.com.dz/api/invoice"

API_KEY = os.environ["API_KEY"]

HEADERS = {"X-Authorization": API_KEY, "Accept": "application/json"}


def create_body(
    *,
    client: str,
    client_email: str,
    invoice_number: int,
    amount: float,
    discount: float,
    back_url: str,
    webhook_url: str,
    mode: str,
    comment: str,
):
    if mode not in EPAY_MODE_OPTIONS:
        raise Exception("Mode payment is not supported")

    return {
        "client": client,
        "client_email": client_email,
        "invoice_number": invoice_number,
        "amount": amount,
        "discount": discount,
        "back_url": back_url,
        "webhook_url": webhook_url,
        "mode": mode,
        "comment": comment,
    }


request_body = create_body(
    client="user 1",
    client_email="example@gmail.com",
    invoice_number=1,
    amount=1000,
    discount=0,
    back_url="https://www.exemple.org/",
    webhook_url="https://www.exemple.org/webhook-validator",
    mode="EDAHABIA",
    comment="first try",
)


request_payment = requests.post(REQUES_URL, json=request_body, headers=HEADERS)


if request_payment.status_code == 201:
    content = json.loads(request_payment.content)
    print(f"got to {content['checkout_url']}")
else:
    print("payment failed")
