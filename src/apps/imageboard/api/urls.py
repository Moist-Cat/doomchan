from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ThreadViewSet, CommentViewSet, BoardViewSet

router = DefaultRouter()
router.register('board', BoardViewSet)
router.register('thread', ThreadViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
