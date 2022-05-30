import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView, BaseDetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from chargily_lib.constant import (
    PAYMENT_CANCELED,
    PAYMENT_PAID,
    PAYMENT_FAILED,
    PAYMENT_IN_PROGRESS,
)

from chargily_epay_django.forms import FakePaymentForm

from chargily_epay_django.models import AbstractPayment
from chargily_epay_django.payment_manager import payment_manager



# logger = logging.getLogger("chargily-app")


class ValidationError(Exception):
    pass


# -----------
# MXIN
# -----------
class OnlyFinishedPaymentMixin:
    def get_queryset(self):
        return self.model._default_manager.filter(
            status__in=[
                PAYMENT_PAID,
                PAYMENT_FAILED,
                PAYMENT_CANCELED,
            ]
        )


# -----------
# VIEW
# -----------
@method_decorator(csrf_exempt, name="dispatch")
class PaymentConfirmationView(View):
    required_body_options = {
        "status",
        "amount",
        "invoice_number",
    }

    manager = payment_manager
    model = None

    def post(self, request: HttpRequest, *args, **kwargs):
        self.get_args(request)
        try:
            self.validate_signature()
            self.validate_args()
            self.confirmation()
        except ValidationError as e:
            # LOG here
            pass

        return HttpResponse()

    def validate_signature(self) -> bool:
        valide = self.manager.make_confirmation(self.raw_body, self.request_signature)
        if not valide:
            raise ValidationError()

    def get_args(self, request: HttpRequest):
        self.request_signature = request.headers.get("Signature")
        self.raw_body = request.body

        self.request_body = json.loads(request.body)

        if self.request_body:
            self.invoice: dict = self.request_body.get("invoice") or None

    def validate_args(self) -> bool:
        if not self.request_signature:
            return False

        if not hasattr(self, "request_body"):
            return False

        if not hasattr(self, "invoice"):
            return False

        if not isinstance(self.invoice, dict):
            return False

        request_args = set(self.invoice.keys())

        if not self.required_body_options.issubset(request_args):
            return False

        return True

    def confirmation(self, *args, **kwargs):
        invoice_number = self.invoice.get("invoice_number")

        object: AbstractPayment = self.get_object(invoice_number)
        if not object:
            raise ObjectDoesNotExist()

        if object.status != PAYMENT_IN_PROGRESS:
            raise ValidationError()

        status = self.invoice.get("status")

        if status == PAYMENT_PAID:
            self.payment_success(object, invoice=self.invoice)
        elif status == PAYMENT_FAILED:
            self.payment_failed(object, invoice=self.invoice)
        elif status == PAYMENT_CANCELED:
            self.payment_canceled(object, invoice=self.invoice)
        else:
            pass
            # TODO: handel unkown status

    def get_object(self, invoice_number):
        object = self.model.objects.get(invoice_number=invoice_number)
        return object

    def payment_success(self, object: AbstractPayment, **kwargs):
        object.payment_confirm(**kwargs)

    def payment_failed(self, object: AbstractPayment, **kwargs):
        object.payment_failed(**kwargs)

    def payment_canceled(self, object: AbstractPayment, **kwargs):
        object.payment_canceled(**kwargs)


class CreatePaymentView(CreateView):
    payment_create_faild_url = None

    def form_valid(self, form) -> HttpResponse:
        self.create_object(form)

        payment_url = self.object.make_payment()
        if payment_url:
            return HttpResponseRedirect(redirect_to=payment_url)

        print("failed")
        return self.payment_create_faild()

    def create_object(self, form):
        self.object: AbstractPayment = form.save()

    def payment_create_faild(self):
        return HttpResponseRedirect(redirect_to=self.payment_create_faild_url)


class PaymentObjectStatusView(DetailView):
    model: AbstractPayment = None
    slug_field: str = "invoice_number"
    slug_url_kwarg = "invoice_number"


class PaymentObjectDoneView(OnlyFinishedPaymentMixin, PaymentObjectStatusView):
    pass


class FakePaymentView(FormView, BaseDetailView):
    slug_field: str = "invoice_number"
    slug_url_kwarg = "invoice_number"
    template_name: str = "chargily_epay_django/fake-payment-view.html"
    form_class = FakePaymentForm

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if "object" not in kwargs:
            kwargs["object"] = self.get_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form: FakePaymentForm):
        self.object = self.get_object()
        payment_status = form.data["status"]

        if payment_status == PAYMENT_PAID:
            self.object.payment_confirm()
        elif payment_status == PAYMENT_CANCELED:
            self.object.payment_canceled()
        elif payment_status == PAYMENT_FAILED:
            self.object.payment_failed()
        return HttpResponseRedirect(self.object.generate_back_url())


# class CreatePaymentJSON(CreatePaymentView):
#     def form_valid(self, form) -> HttpResponse:
#         self.create_object()
#         payment_url = self.object.make_payment()
#         if payment_url:
#             return JsonResponse({"redirect_url": payment_url, "status": "success"})
#         return JsonResponse(
#             {"redirect_url": self.payment_create_faild_url, "status": "failed"}
#         )
