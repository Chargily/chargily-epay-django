# epay-gateway-django
Chargily ePay Gateway (Django Package)

![Chargily ePay Gateway](https://raw.githubusercontent.com/Chargily/epay-gateway-php/main/assets/banner-1544x500.png "Chargily ePay Gateway")

This Plugin is to integrate ePayment gateway with Chargily easily.
- Currently support payment by **CIB / EDAHABIA** cards and soon by **Visa / Mastercard** 
- This repo is recently created for **Django plugin**, If you are a developer and want to collaborate to the development of this plugin, you are welcomed!

# Requirements
1. Python 2.7 or higher.
2. Django 1.11 or higher.
3. API Key/Secret from [ePay by Chargily](https://epay.chargily.com.dz) dashboard for free.

# Installation
Using pip (Recomended) ***Not in production yet.***
```bash
pip install chargily_epay_gateway_django
```

# Quick start
Set `CHARGILY_APP_KEY` and `CHARGILY_APP_SECRET` in your settings.py file with the secret key and app key from [ePay Dashboard][api-keys]

**(Make sure to save them inside `.env`, then load them in settings.py )**

# Usage
1- Make Payment:

- You can use class or function based view to make a payment
- If you are using `POST` method, make sure to *disable Django's CSRF validation*.

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chargily_epay_gateway.api import make_payment

@csrf_exempt
def invoice(request):
    if request.method != 'POST':
        return HttpResponse(f'Method {request.method} not allowed')
    response = make_payment(
        client='Client Name',
        client_email='Client Email',
        invoice_number='Invoice ID',
        amount='Amount',
        discount='Discount',
        back_url='https://example.com/',
        webhook_url='https://example.com/webhook/',
        mode="CIB",
        comment='for integration test',
    )
    return JsonResponse(response.json(), status=response.status_code)
```

2- Validate Chargily Signature:

```python
from chargily_epay_gateway.api import webhook_is_valid

# Return True if signature is valid, otherwise False
valid_signature = webhook_is_valid(request)
```

# Configurations

- Available Configurations

| key                   |  description                                                                                          | redirect url |  process url |
|-----------------------|-------------------------------------------------------------------------------------------------------|--------------|--------------|
| CHARGILY_APP_KEY               | must be string given by organization                                                                  |   required   |   required   |
| CHARGILY_APP_SECRET            | must be string given by organization                                                                  |   required   |   required   |
| back_url        | must be string and valid url                                                                          |   required   | not required |
| webhook_url        | must be string and valid url                                                                          _|   required   | required |
| mode                  | must be in **CIB**,**EDAHABIA**                                                                       |   required   | not required |
| invoice_number       |  string or int                                                                                 |   required   | not required |
| client_name  | string                                                                                        |   required   | not required |
| clientEmail | must be valid email This is where client receive payment receipt after confirmation        |   required   | not required |
| amount      | must be numeric and greather or equal than  75                                                        |   required   | not required |
| discount    | must be numeric and between 0 and 99  (discount in %)                                     |   required   | not required |
| description  | must be string_                                                                                        |   required   | not required |


# Testing

Tests are in progress...


# Notice

- If you faced Issues [Click here to open one](https://github.com/BeleganStartup/epay-gateway-django/issues/new)