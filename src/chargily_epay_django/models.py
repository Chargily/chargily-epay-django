from django.utils import timezone
from django.urls import reverse
from django.db import models

from chargily_epay_django.payment_manager import payment_manager
from chargily_epay_django.utils import get_webhook_url

from chargily_lib.utils import extract_redirect_url
from chargily_lib.invoice import new_invoice
from chargily_lib.constant import (
    PAYMENT_FAILED,
    PAYMENT_CANCELED,
    PAYMENT_PAID,
    PAYMENT_EXPIRED,
    PAYMENT_IN_PROGRESS,
    # ---
    EDAHABIA,
    CIB,
)


class FakePaymentMixin:
    fake_payment_url = "fake-payment"

    def make_payment(self):
        redirect_url = reverse(
            self.fake_payment_url, kwargs={"invoice_number": self.invoice_number}
        )
        return redirect_url


class AbstractPayment(models.Model):
    back_url = None
    webhook_url = None

    PAYMENT_MODE = {
        (CIB, "CIB"),
        (EDAHABIA, "EDAHABIA"),
    }

    PAYMENT_STATUS = {
        (PAYMENT_EXPIRED, "EXPIRED"),
        (PAYMENT_IN_PROGRESS, "IN PROGRESS"),
        (PAYMENT_PAID, "PAID"),
        (PAYMENT_FAILED, "FAILED"),
        (PAYMENT_CANCELED, "CANCELED"),
    }

    invoice_number = models.BigAutoField(primary_key=True)  # PRIMARY KEY
    amount = models.DecimalField(decimal_places=2, max_digits=1000000)
    comment = models.TextField()

    discount = models.FloatField(max_length=2, default=0, blank=True)
    mode = models.CharField(max_length=25, choices=PAYMENT_MODE, default=EDAHABIA)

    status = models.CharField(
        max_length=25, default=PAYMENT_IN_PROGRESS, choices=PAYMENT_STATUS
    )

    # Metadata
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_payment_data(self) -> dict:
        request_data = new_invoice()

        request_data["invoice_number"] = self.invoice_number
        request_data["client"] = self.get_client()
        request_data["amount"] = float(self.amount)
        request_data["comment"] = self.comment
        request_data["discount"] = self.discount
        request_data["mode"] = self.mode
        request_data["client_email"] = self.get_client_email()
        request_data["webhook_url"] = self.generate_webhook_url()
        request_data["back_url"] = self.generate_back_url()
        return request_data

    def generate_webhook_url(self):
        confirmaion_url = str(reverse(self.webhook_url))
        return get_webhook_url(confirmaion_url)

    def generate_back_url(self):
        confirmaion_url = str(reverse(self.back_url))
        return get_webhook_url(confirmaion_url)

    def get_client_email(self):
        raise NotImplementedError()

    def get_client(self):
        raise NotImplementedError()

    def make_payment(self):
        request_data = self.get_payment_data()
        response = payment_manager.make_payment(request_data)
        if response.status_code == 201:
            return extract_redirect_url(response.content)
        else:
            self.payment_failed()
            return None


    def payment_confirm(self, **kwargs):
        self.status = PAYMENT_PAID
        self.payment_date = timezone.now()
        self.save()

    def payment_expired(self, **kwargs):
        self.status = PAYMENT_EXPIRED
        self.save()

    def payment_failed(self, **kwargs):
        self.status = PAYMENT_FAILED
        self.save()

    def payment_canceled(self, **kwargs):
        self.status = PAYMENT_CANCELED
        self.save()


class AuthPayment(AbstractPayment):
    client = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    client_email = models.EmailField()

    def get_client_email(self):
        return self.client_email

    def get_client(self):
        return self.client.username

    class Meta:
        abstract = True


class AnonymPayment(AbstractPayment):
    client = models.CharField(max_length=255)
    client_email = models.EmailField()

    def get_client_email(self):
        return self.client_email

    def get_client(self):
        return self.client

    class Meta:
        abstract = True

