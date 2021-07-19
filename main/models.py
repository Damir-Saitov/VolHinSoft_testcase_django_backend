from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Board(models.Model):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    name = models.CharField(
        verbose_name='name',
        max_length=32,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='boards',
        editable=False,
    )

    def __str__(self):
        return self.name


class Column(models.Model):
    class Meta:
        verbose_name = 'Колонка'
        verbose_name_plural = 'Колонки'

    name = models.CharField(
        verbose_name='name',
        max_length=32,
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='columns',
        editable=False,
    )

    def __str__(self):
        return self.name


class Card(models.Model):
    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Корточки'

    name = models.CharField(
        verbose_name='name',
        max_length=32,
    )
    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        related_name='cards',
    )

    def __str__(self):
        return self.name
