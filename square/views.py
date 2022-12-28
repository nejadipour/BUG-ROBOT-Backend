from rest_framework.viewsets import ModelViewSet
from .serializers import SquareSerializer
from .models import Square
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


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
    def add_card(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        if square.is_occupied:
            return Response(
                data={"message": "This position is occupied"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            square_type = request.data["square_type"]

            square.square_type = square_type
            square.is_occupied = True
            square.save()

            serializer = SquareSerializer([square], many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def move(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        destination_id = request.data["destination"]

        if square.square_type != "BOT":
            return Response(
                data={"message": "You can't move this card"},
                status=status.HTTP_400_BAD_REQUEST)

        destination = Square.objects.filter(id=destination_id).last()
        if destination.is_occupied:
            return Response(
                data={"message": "The position is occupied"},
                status=status.HTTP_400_BAD_REQUEST)

        if destination.position_x == square.position_x:
            distance = abs(destination.position_y - square.position_y)
        elif destination.position_y == square.position_y:
            distance = abs(destination.position_x - square.position_x)
        else:
            return Response(
                data={"message": "You can move only in right-left or bottom-top direction"},
                status=status.HTTP_400_BAD_REQUEST)

        if distance > square.board.robot_strength:
            return Response(
                data={"message": "This position is too far."},
                status=status.HTTP_400_BAD_REQUEST)

        destination.square_type = square.square_type
        destination.is_occupied = True
        destination.save()

        square.square_type = "EMT"
        square.is_occupied = False
        square.save()

        serializer = SquareSerializer([destination, square], many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def attack(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        robot_strong = square.board.robot_strength

        right = square.position_x + robot_strong
        left = square.position_x - robot_strong
        top = square.position_y + robot_strong
        bottom = square.position_y - robot_strong

        neighbors = Square.objects.filter(~Q(id=square.id), board=square.board, position_x__gte=left,
                                          position_x__lte=right, position_y__gte=bottom, position_y__lte=top)

        neighbors.update(is_occupied=False, square_type="EMT")

        serializer = SquareSerializer(neighbors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
