from rest_framework.routers import DefaultRouter
from .views import AutomationCategoryViewSet, AutomationTemplateViewSet, AutomationViewSet

router = DefaultRouter()
router.register(r'categories', AutomationCategoryViewSet)
router.register(r'templates', AutomationTemplateViewSet)
router.register(r'automations', AutomationViewSet)

urlpatterns = router.urls
