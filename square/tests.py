from django.test import TestCase, Client
from django.urls import reverse
from board.models import Board
from rest_framework import status
from .models import Square


class TestUrls(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.board = Board.objects.create(
            name="testing board", row=3, column=3, robot_strength=1)

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

    def test_move(self):
        square = Square.objects.filter(board=self.board).first()
        square.square_type = "BUG"
        square.save()

        destination = Square.objects.filter(
            board=self.board, position_x=square.position_x+2, position_y=square.position_y).first()

        # square id not available
        url = reverse('square-move', kwargs={"pk": -1})
        response = self.client.post(url+f"?destination={destination.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # trying to move a bug instead of robot
        url = reverse('square-move', kwargs={"pk": square.id})
        response = self.client.post(url+f"?destination={destination.id}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        square.square_type = "BOT"
        square.save()

        # destinaton id not available
        url = reverse('square-move', kwargs={"pk": square.id})
        response = self.client.post(url+f"?destination=-1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # trying to a far position
        response = self.client.post(url+f"?destination={destination.id}")
        print(destination)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        destination = Square.objects.filter(
            board=self.board, position_x=square.position_x+1, position_y=square.position_y).first()

        destination.is_occupied = True
        destination.save()

        # moving to an occupied position
        response = self.client.post(url+f"?destination={destination.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        destination.is_occupied = False
        destination.save()
        response = self.client.post(url+f"?destination={destination.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
