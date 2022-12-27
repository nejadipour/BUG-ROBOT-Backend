from django.db import models
from board.models import Board


class Square(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, null=False, blank=False)
    position_x = models.IntegerField(null=False, blank=False)
    position_y = models.IntegerField(null=False, blank=False)
    is_occupied = models.BooleanField(default=False, null=False)

    SQUARE_TYPES = [
        ('EMT', 'empty'),
        ('BOT', 'robot'),
        ('BUG', 'bug')
    ]

    square_type = models.CharField(
        max_length=3,
        choices=SQUARE_TYPES,
        default='EMT',
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.board}: [{self.position_x}, {self.position_y}]"
