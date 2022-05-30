from django.forms import ChoiceField, Form, CharField, ModelForm
from chargily_lib.constant import (
    PAYMENT_FAILED,
    PAYMENT_CANCELED,
    PAYMENT_PAID,
)


class FakePaymentForm(Form):
    PAYMENT_STATUS = {
        (PAYMENT_PAID, "PAID"),
        (PAYMENT_FAILED, "FAILED"),
        (PAYMENT_CANCELED, "CANCELED"),
    }

    status = ChoiceField(choices=PAYMENT_STATUS)

        