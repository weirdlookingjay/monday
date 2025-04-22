from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

class TestAuthErrorView(APIView):
    def get(self, request):
        raise AuthenticationFailed("This is a test auth error from DRF.")
