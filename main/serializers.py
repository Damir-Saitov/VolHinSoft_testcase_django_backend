from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('username', 'password', 'email')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = '__all__'


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Column
        fields = '__all__'

    board = serializers.IntegerField(source='board_id')

    def validate_board(self, value):
        error = serializers.ValidationError(detail={
            'board': 'Invalid value',
        })

        try:
            board = models.Board.objects.get(pk=value)
        except models.Board.DoesNotExist:
            raise error

        if (board.user.pk != self.context['request'].user.pk):
            raise error

        return value


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = '__all__'

    column = serializers.IntegerField(source='column_id')

    def validate_column(self, value):
        error = serializers.ValidationError(detail={
            'column': 'Invalid value',
        })

        try:
            column = models.Column.objects.get(pk=value)
        except models.Column.DoesNotExist:
            raise error

        if (column.board.user.pk != self.context['request'].user.pk):
            raise error

        return value
