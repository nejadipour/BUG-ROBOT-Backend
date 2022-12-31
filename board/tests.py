from django.test import TestCase, Client
from rest_framework import status
from square.models import Square
from .models import Board


class TestEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_create(self):
        response = self.client.post("/board/",
                                    data={"name": "new test baord", "row": 2, "column": 2, "robot_strength": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        squares = Square.objects.filter(board=response.data["id"])
        self.assertEqual(len(squares), 2*2)

    def test_destroy(self):
        board = Board.objects.create(name="test destroy board", row=2, column=2, robot_strength=1)
        response = self.client.delete(f"/board/{board.id}/")

        squares = Square.objects.filter(board=board)
        self.assertEqual(len(squares), 0)
