from rest_framework import serializers
from .models import Square


class SquareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Square
        fields = '__all__'
