from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.utils import IntegrityError

from . import models, serializers


class UserView(ViewSet):
    serializer_class = serializers.UserSerializer

    @action(
        detail=False,
        methods=('POST',),
        authentication_classes=tuple(),
        permission_classes=tuple(),
    )
    def registration(self, request: Request) -> Response:
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        try:
            user = models.UserModel.objects.create_user(**user.data)
        except IntegrityError as error:
            return Response(
                data={'message': error.args[0]},
                status=400,
            )
        user.save()
        return Response()


class BoardView(ModelViewSet):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user.pk)

    def perform_create(self, serializer: serializers.BoardSerializer):
        serializer.save(user=self.request.user)


class ColumnView(ModelViewSet):
    serializer_class = serializers.ColumnSerializer

    def get_queryset(self):
        columns = models.Column.objects.filter(
            board__in=models.Board.objects.filter(
                user=self.request.user.pk
            )
        )

        board = self.request.query_params.get('board')
        if board is None:
            return columns

        return columns.filter(board=board)


class CardView(ModelViewSet):
    serializer_class = serializers.CardSerializer

    def get_queryset(self):
        cards = models.Card.objects.filter(
            column__in=models.Column.objects.filter(
                board__in=models.Board.objects.filter(
                    user=self.request.user.pk
                )
            )
        )

        column = self.request.query_params.get('board')
        if column is None:
            return cards

        return cards.filter(column=column)
