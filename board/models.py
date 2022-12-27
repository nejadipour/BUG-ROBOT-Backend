from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    row = models.IntegerField(null=False, blank=False)
    column = models.IntegerField(null=False, blank=False)
    robot_strength = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name
