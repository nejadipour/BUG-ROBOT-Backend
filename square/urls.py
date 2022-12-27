from rest_framework.routers import DefaultRouter
from .views import SquareViewSet


router = DefaultRouter()
router.register(r'square', SquareViewSet, basename='square')

urlpatterns = router.urls
