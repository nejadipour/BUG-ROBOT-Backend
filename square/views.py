from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import SquareSerializer
from .models import Square
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from .parameters import square_type_param, destination_param, board_param


class SquareViewSet(ReadOnlyModelViewSet):
    serializer_class = SquareSerializer
    queryset = Square.objects.all()

    @swagger_auto_schema(
        manual_parameters=[board_param],
        operation_description="The squares of the passed board id will be reurned with postions as key",
        responses={
            "200": "squares of the board returned successfully"})
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

    @swagger_auto_schema(
        manual_parameters=[square_type_param],
        operation_description="By passing the id and type, you can add a card to any square",
        responses={
            "404": "square id not available",
            "200": "card added to the square. updated square will be returned.",
            "400": "occupied position"})
    @action(detail=True, methods=['POST'])
    def add_card(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        if square is None:
            return Response(
                data={"message": "Square not available"},
                status=status.HTTP_404_NOT_FOUND)
        if square.is_occupied:
            return Response(
                data={"message": "This position is occupied"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            square_type = self.request.query_params.get('square_type')

            square.square_type = square_type
            square.is_occupied = True
            square.save()

            serializer = SquareSerializer([square], many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[destination_param],
        operation_description="By passing the current id and destination's id, you can move a card to the position",
        responses={
            "404": "square or destination not available",
            "200": "move done successfully. changed squares will be returned",
            "400": "selected square type is not BOT - destination is occupied - impossible direction for move - distance more than robot's strength"})
    @action(detail=True, methods=['POST'])
    def move(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        destination_id = self.request.query_params.get('destination')

        if square is None:
            return Response(
                data={"message": "Square not available"},
                status=status.HTTP_404_NOT_FOUND)

        if square.square_type != "BOT":
            return Response(
                data={"message": "You can't move this card"},
                status=status.HTTP_400_BAD_REQUEST)

        destination = Square.objects.filter(id=destination_id).last()
        if destination is None:
            return Response(
                data={"message": "Destination not available"},
                status=status.HTTP_404_NOT_FOUND)

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
                data={
                    "message": "You can move only in right-left or bottom-top direction"},
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

    @swagger_auto_schema(
        operation_description="The neighbors around the passed id will be destroyed",
        responses={
            "404": "square is not available",
            "200": "all the neighbors destroyed",
            "400": "selected square type is not BOT"})
    @action(detail=True, methods=['POST'])
    def attack(self, request, pk, *args, **kwargs):
        square = Square.objects.filter(id=pk).last()
        if square is None:
            return Response(
                data={"message": "Square not available"},
                status=status.HTTP_404_NOT_FOUND)
        robot_strong = square.board.robot_strength

        if square.square_type != "BOT":
            return Response(
                data={"message": "This card doesn't attack others"},
                status=status.HTTP_400_BAD_REQUEST)

        right = square.position_x + robot_strong
        left = square.position_x - robot_strong
        top = square.position_y + robot_strong
        bottom = square.position_y - robot_strong

        neighbors = Square.objects.filter(~Q(id=square.id), ~Q(square_type="BOT"), board=square.board, position_x__gte=left,
                                          position_x__lte=right, position_y__gte=bottom, position_y__lte=top)

        neighbors.update(is_occupied=False, square_type="EMT")

        serializer = SquareSerializer(neighbors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
