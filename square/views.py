from rest_framework.viewsets import ModelViewSet
from .serializers import SquareSerializer
from .models import Square


class SquareViewSet(ModelViewSet):
    serializer_class = SquareSerializer
    queryset = Square.objects.all()
