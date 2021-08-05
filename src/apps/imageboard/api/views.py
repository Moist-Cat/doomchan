from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .serializers import (
    ThreadSerializer,
    CommentSerializer,
    BoardSerializer,
    ThreadFullSerializer
)
from ..models import Thread, Comment, Board

class BoardViewSet(ReadOnlyModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    full_serializer_class = ThreadFullSerializer
    search_fields = ['board__slug', 'title', 'text']
    
    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        if self.lookup_field:
           return self.full_serializer_class
        return self.serializer_class

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
    search_fields = ['comment__thread', 'comment']
