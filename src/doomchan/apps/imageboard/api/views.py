from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import (
    ThreadSerializer,
    CommentSerializer,
    BoardSerializer,
    ThreadFullSerializer,
)
from .permissions import PostTokenValidation
from ..models import Thread, Comment, Board

def get_client_ip(request):
    return request.META.get("REMOTE_ADDR")

class BoardList(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardCatalog(RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = "slug"
    
    def retrieve(self, request, *args, **kwargs):
        """Modified to paginate threads together with the filtering"""
        instance = self.get_object()
        
        self.search_fields = ["text"]
        threads = self.filter_queryset(instance.threads.all())

        page = self.paginate_queryset(threads)

        serializer = self.get_serializer(instance)

        if page is not None:
            thr_serializer = ThreadSerializer(page, many=True)
            thr_pages = self.get_paginated_response(thr_serializer.data)
        res = Response(serializer.data)
        res.data["threads"] = thr_pages.data
        return res
        


class ThreadViewSet(ModelViewSet):
    queryset = Thread.active.all()
    serializer_class = ThreadFullSerializer
    lookup_field = "pk"

    permission_classes = [PostTokenValidation]

    def perform_create(self, serializer):
        serializer.validated_data["ip"] = get_client_ip(self.request)
        serializer.save()

class CommentViewSet(ModelViewSet):
    queryset = Comment.active.all()
    serializer_class = CommentSerializer
    
    permission_classes = [PostTokenValidation]
    
    def perform_create(self, serializer):
        serializer.validated_data["ip"] = get_client_ip(self.request)
        serializer.save()
