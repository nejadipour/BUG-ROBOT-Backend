from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Board
from square.models import Square

@receiver(post_save, sender=Board)
def create_board_squares(sender, instance, created, **kwargs):
    if created:
        for position_x in range(int(instance.column)):
            for position_y in range(int(instance.row)):
                Square.objects.create(
                    board=instance, position_x=position_x, position_y=position_y)
