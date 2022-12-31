from rest_framework.viewsets import ModelViewSet
from .serializers import BoardSerializer
from .models import Board
from square.models import Square
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    @swagger_auto_schema(operation_description="By creating the board, its squares will be created too")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="By deleting the board, its squares will be deleted too")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
