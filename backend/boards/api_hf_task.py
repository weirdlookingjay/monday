from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.hf_task_parser import extract_entities
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view

from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'detail': 'CSRF cookie set'})

from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nlp_create_task(request):
    print("User:", request.user)
    print("Auth:", request.auth)
    text = request.data.get('text', '')
    if not text:
        return Response({'error': 'Missing text'}, status=400)
    try:
        result = extract_entities(text)
        # result contains 'entities' and 'parsed_date'
        return Response({**result, 'raw': text})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
