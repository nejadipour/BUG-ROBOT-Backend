from rest_framework.routers import DefaultRouter
from .views import BoardViewSet


router = DefaultRouter()
router.register(r'board', BoardViewSet, basename='board' )

urlpatterns = router.urls
