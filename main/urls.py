from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.BoardListView.as_view()),
    path('board/<int:pk>/', views.BoardDetailView.as_view()),
    path('column/', views.ColumnListView.as_view()),
    path('column/<int:pk>/', views.ColumnDetailView.as_view()),
    path('card/', views.CardListView.as_view()),
    path('card/<int:pk>/', views.CardDetailView.as_view()),
]