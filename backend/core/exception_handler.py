from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and hasattr(exc, 'detail'):
        response.data['detail'] = str(exc.detail)
        response.data['type'] = exc.__class__.__name__
    return response
