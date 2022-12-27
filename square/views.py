from rest_framework.viewsets import ModelViewSet
from .serializers import SquareSerializer
from .models import Square


class SquareViewSet(ModelViewSet):
    serializer_class = SquareSerializer

    def get_queryset(self):
        board = self.request.query_params.get('board')

        if not board:
            return Square.objects.all()
        else:
            return Square.objects.filter(board=board)
