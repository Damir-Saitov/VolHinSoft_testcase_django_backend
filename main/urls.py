from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserView, basename='user')
router.register('board', views.BoardView, basename='board')
router.register('column', views.ColumnView, basename='column')
router.register('card', views.CardView, basename='card')

urlpatterns = router.urls
