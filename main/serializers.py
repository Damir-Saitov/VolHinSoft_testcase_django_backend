from rest_framework import serializers

from . import models


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Column
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = '__all__'
