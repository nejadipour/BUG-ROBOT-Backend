from django.test import TestCase, Client
from django.urls import reverse
from board.models import Board
from rest_framework import status
from .models import Square


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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url+f"?board={-1}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_card(self):
        url = reverse('square-add-card', kwargs={"pk": -1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        square = Square.objects.filter(board=self.board).first()
        url = reverse('square-add-card', kwargs={"pk": square.id})
        response = self.client.post(url+"?square_type=BOT/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url+"?square_type=BOT/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
