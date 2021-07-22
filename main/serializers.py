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

    # Если не указать явно, то:
    # IntegrityError at /api/column/
    # NOT NULL constraint failed: main_column.board_id
    # Может быть баг из-за название таблицы "Column"
    board = serializers.IntegerField(source='board_id')

    def validate_board(self, value: int):
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

    # column = serializers.IntegerField(source='column_id')

    def validate_column(self, value: models.Column):
        if (value.board.user.pk != self.context['request'].user.pk):
            raise serializers.ValidationError(detail={
                'column': 'Invalid value',
            })

        return value
