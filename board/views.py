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
        data = request.data
        board = Board.objects.create(
            name=data["name"], row=data["row"], column=data["column"], robot_strength=data["robot_strength"])

        for position_x in range(int(board.column)):
            for position_y in range(int(board.row)):
                Square.objects.create(
                    board=board, position_x=position_x, position_y=position_y)

        serializer = self.get_serializer(board)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_description="By deleting the board, its squares will be deleted too")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
