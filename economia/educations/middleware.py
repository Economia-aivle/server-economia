# myapp/middleware.py
from django.shortcuts import redirect

class ResetCorrectCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/educations/multiple/'):
            request.session['correct_count'] = 0

        return response


