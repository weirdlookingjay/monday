from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ActivityLog, ActivityLogRead
from .serializers import ActivityLogSerializer

class ActivityLogMarkReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        log = get_object_or_404(ActivityLog, pk=pk)
        ActivityLogRead.objects.get_or_create(user=request.user, log=log)
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)

class ActivityLogListAPIView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ActivityLog.objects.order_by('-timestamp')
        unread = self.request.query_params.get('unread')
        user = self.request.user
        if unread:
            # Only show logs the user has NOT read
            return qs.exclude(reads__user=user)[:50]
        return qs[:50]
