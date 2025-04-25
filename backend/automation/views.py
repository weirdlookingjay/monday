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

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    def update(self, request, *args, **kwargs):
        # PATCH/PUT for editing an automation
        logging.warning(f"[AutomationViewSet] UPDATE called with data: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # DELETE for deleting an automation
        logging.warning(f"[AutomationViewSet] DESTROY called for id: {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='duplicate')
    def duplicate(self, request, pk=None):
        # Custom action to duplicate an automation
        try:
            orig = self.get_object()
            data = self.get_serializer(orig).data
            data.pop('id', None)
            data['name'] = (data.get('name') or '') + ' (Copy)'
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            new_automation = serializer.save(user=request.user)
            return Response(self.get_serializer(new_automation).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f"[AutomationViewSet] DUPLICATE error: {e}")
            return Response({'detail': 'Could not duplicate automation.'}, status=status.HTTP_400_BAD_REQUEST)


