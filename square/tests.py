from django.test import TestCase, Client
from django.urls import reverse
from board.models import Board
from rest_framework import status


class TestUrls(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.board = Board.objects.create(name="testing board", row=2, column=2, robot_strength=1)

    def test_square_list_url(self):
        url = reverse('square-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_board_squares(self):
        url = reverse('square-get-board-squares')
        response = self.client.get(url+f"?board={self.board.id}")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url+f"?board={-1}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
