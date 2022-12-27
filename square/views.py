from rest_framework.viewsets import ModelViewSet
from .serializers import SquareSerializer
from .models import Square
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class SquareViewSet(ModelViewSet):
    serializer_class = SquareSerializer

    def get_queryset(self):
        board = self.request.query_params.get('board')

        if not board:
            return Square.objects.all()
        else:
            return Square.objects.filter(board=board)

    @action(detail=False, methods=['GET'])
    def get_board_squares(self, request, *args, **kwargs):
        board = self.request.query_params.get('board')

        squares = Square.objects.filter(board=board)
        data = {}

        serializer = SquareSerializer(squares, many=True)

        for square in serializer.data:
            position_x = square["position_x"]
            position_y = square["position_y"]
            data[f"[{position_x},{position_y}]"] = dict(square)

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def move(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        destination_id = request.data["destination"]

        destination = Square.objects.filter(id=destination_id).last()
        destination.square_type = square.square_type
        destination.is_occupied = True
        destination.save()
        
        square.square_type = "EMT"
        square.is_occupied = False
        square.save()
        
        serializer = SquareSerializer([destination, square], many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
