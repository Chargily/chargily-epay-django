from django.http import JsonResponse

from .exceptions import ChargilyErrorBase


class ChargilyExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ChargilyErrorBase):
            return JsonResponse({
                'error_code': exception.error_code,
                'error_msg': exception.chargily_msg,
            }, status=422)
        return None
