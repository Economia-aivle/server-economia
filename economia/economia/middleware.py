from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from economia.models import TokenBlacklistBlacklistedtoken, TokenBlacklistOutstandingtoken
from rest_framework.response import Response
from rest_framework import status

class AddValueToRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.custom_value = ''  # 원하는 값을 추가합니다.
        response = self.get_response(request)
        return response



class BlacklistTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split()[1]  # Bearer <token>에서 token 추출
            print("SSSSSSSS: ",token)

            try:
                # AccessToken 검증
                AccessToken(token)

                # 블랙리스트 확인
                outstanding_token = TokenBlacklistOutstandingtoken.objects.filter(token=token).first()
                print("AAAAAA:",outstanding_token)
                if outstanding_token and TokenBlacklistBlacklistedtoken.objects.filter(token=outstanding_token).exists():
                    print("Token is blacklisted.")
                    return Response({"detail": "Access token is blacklisted."}, status=status.HTTP_403_FORBIDDEN)

            except TokenError:
                return Response({"detail": "Invalid token."}, status=status.HTTP_403_FORBIDDEN)
