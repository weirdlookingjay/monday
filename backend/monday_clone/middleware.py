from django.utils.deprecation import MiddlewareMixin

class DebugRequestHeadersMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/boards/list/'):
            print('\n[DEBUG][MIDDLEWARE] Incoming headers for', request.path)
            for k, v in request.headers.items():
                print(f'    {k}: {v}')
        return None
