from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

from . import models


class IfColumnInUserBoard(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        try:
            column = models.Column.objects.get(pk=view.kwargs['pk'])
        except models.Column.DoesNotExist:
            return False

        return column.board.user.pk == request.user.pk


class IfCardInUserBoard(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        try:
            card = models.Card.objects.get(pk=view.kwargs['pk'])
        except models.Card.DoesNotExist:
            return False

        return card.column.board.user.pk == request.user.pk


class IfColumnInDataInUserBoard(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        column_id = request.data.get('column')
        if column_id is not None:
            try:
                column = models.Column.objects.get(pk=column_id)
            except models.Column.DoesNotExist:
                return False

            return column.board.user.pk == request.user.pk

        return True
