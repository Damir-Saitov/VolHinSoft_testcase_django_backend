from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from . import models, serializers, permissions


def required_query(*query_names: str):
    def wrapper(func):
        def wrapped(self, request: Request, *args, **kwargs):
            no_found_query = []
            for query_name in query_names:
                if request.query_params.get(query_name) is None:
                    no_found_query.append(query_name)
            if len(no_found_query):
                query_names_string = ', '.join(f"'{query}'" for query in no_found_query)
                return Response(data={
                    'detail': f'{query_names_string} query param is required'
                }, status=400)
            
            return func(self, request, *args, **kwargs)
        return wrapped
    return wrapper


class BoardListView(ListCreateAPIView):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer: serializers.BoardSerializer):
        serializer.save(user=self.request.user)

class BoardDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return models.Board.objects.filter(user=self.request.user.pk)


def getBoardIfInUserBoard(request: Request, board_id: int) -> models.Board:
    '''
    Raises
    ------
    PermissionDenied
        если доска не принадлежит текущему пользователю
    '''
    try:
        board = models.Board.objects.get(pk=board_id)
    except models.Board.DoesNotExist:
        raise PermissionDenied()

    if board.user.pk != request.user.pk:
        raise PermissionDenied()

    return board

class ColumnListView(APIView):
    serializer_class = serializers.ColumnSerializer

    @required_query('board')
    def get(self, request: Request) -> Response:
        return Response(serializers.ColumnSerializer(
            models.Column.objects.filter(
                board=getBoardIfInUserBoard(request, request.query_params.get('board')
            )),
            many=True,    
        ).data)
    
    def post(self, request: Request) -> Response:
        column = serializers.ColumnSerializer(data=request.data)
        column.is_valid(raise_exception=True)
        column.save(board=getBoardIfInUserBoard(request, request.data['board']))
        return Response(column.data)

class ColumnDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (
        *RetrieveUpdateDestroyAPIView.permission_classes,
        permissions.IfColumnInUserBoard,
    )
    serializer_class = serializers.ColumnSerializer
    queryset = models.Column.objects.all()


def getColumnIfInUserBoard(request: Request, column_id: int) -> models.Column:
    '''
    Raises
    ------
    PermissionDenied
        если колонка не принадлежит текущему пользователю
    '''
    try:
        column = models.Column.objects.get(pk=column_id)
    except models.Column.DoesNotExist:
        raise PermissionDenied()

    if column.board.user.pk != request.user.pk:
        raise PermissionDenied()

    return column

class CardListView(APIView):
    serializer_class = serializers.CardSerializer

    @required_query('column')
    def get(self, request: Request) -> Response:
        return Response(serializers.CardSerializer(
            models.Card.objects.filter(
                column=getColumnIfInUserBoard(request, request.query_params.get('column')
            )),
            many=True,    
        ).data)
    
    def post(self, request: Request) -> Response:
        card = serializers.CardSerializer(data=request.data)
        card.is_valid(raise_exception=True)
        card.save(column=getColumnIfInUserBoard(request, request.data['column']))
        return Response(card.data)

class CardDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (
        *RetrieveUpdateDestroyAPIView.permission_classes,
        permissions.IfCardInUserBoard,
        permissions.IfColumnInDataInUserBoard,
    )
    serializer_class = serializers.CardSerializer
    queryset = models.Card.objects.all()
