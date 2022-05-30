from chargily_lib.constant import CHARGILY_API_URL
from chargily_lib.sync_lib.webhook import PaymentManager
from django.conf import settings

_api_url: str
try:
    _api_url = settings.CHARGILY_API_URL
except Exception as e:
    _api_url = CHARGILY_API_URL

payment_manager = PaymentManager(
    settings.CHARGILY_API_KEY, settings.CHARGILY_SECRET_KEY, _api_url
)
