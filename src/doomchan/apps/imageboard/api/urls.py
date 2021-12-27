from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ThreadViewSet, CommentViewSet, BoardList, BoardCatalog

router = DefaultRouter()
router.register("thread", ThreadViewSet)
router.register("comment", CommentViewSet)

urlpatterns = [
    path("board/", BoardList.as_view()),
    path("board/<slug:slug>", BoardCatalog.as_view()),
    path("", include(router.urls))
]
