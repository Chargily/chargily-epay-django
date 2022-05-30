from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

def get_webhook_url(webhook_url, site_url=None):
    if site_url:
        return urljoin(site_url, webhook_url)

    if settings.DEBUG:
        return urljoin(settings.CHARGILY_FAKE_DOMAIN, webhook_url)
    else:
        return urljoin(settings.CHARGILY_SITE, webhook_url)
