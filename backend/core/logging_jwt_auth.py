from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

class LoggingJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        logging.warning(f"[LoggingJWTAuthentication] Authorization header: {auth_header}")
        try:
            result = super().authenticate(request)
            logging.warning(f"[LoggingJWTAuthentication] Authentication result: {result}")
            return result
        except Exception as e:
            logging.error(f"[LoggingJWTAuthentication] Exception: {e}")
            raise
