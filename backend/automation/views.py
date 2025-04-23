from rest_framework import viewsets, permissions
from .models import AutomationCategory, AutomationTemplate, Automation
from .serializers import AutomationCategorySerializer, AutomationTemplateSerializer, AutomationSerializer

class AutomationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AutomationCategory.objects.all()
    serializer_class = AutomationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class AutomationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AutomationTemplate.objects.all()
    serializer_class = AutomationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

import logging

class AutomationViewSet(viewsets.ModelViewSet):
    queryset = Automation.objects.all()
    serializer_class = AutomationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        logging.warning(f"[AutomationViewSet] request.user: {request.user} (is_authenticated={request.user.is_authenticated})")
        logging.warning(f"[AutomationViewSet] request.auth: {request.auth}")
        logging.warning(f"[AutomationViewSet] headers: {dict(request.headers)}")

    def get_queryset(self):
        user = self.request.user
        return Automation.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        logging.warning(f"[AutomationViewSet] CREATE called with data: {request.data}")
        response = super().create(request, *args, **kwargs)
        logging.warning(f"[AutomationViewSet] CREATE response: {response.data}")
        return response


