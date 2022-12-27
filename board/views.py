from rest_framework.viewsets import ModelViewSet
from .serializers import BoardSerializer
from .models import Board


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
