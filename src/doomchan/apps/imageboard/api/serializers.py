from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.http import Http404
from ..models import Board, Thread, Comment

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["pk", "name", "comment", "thread", "image", "created"]
        
class ThreadSerializer(ModelSerializer):

    class Meta:
        model = Thread
        exclude = ["ip"]

class ThreadFullSerializer(ThreadSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ["pk", "name", "title", "text", "comments", "board", "image"]
    
    def validate(self, attrs):
        board = attrs["board"]
        if isinstance(attrs["board"], str):
            try:
                board = Board.objects.get(slug=board)
                attrs["board"] = board
            except Board.DoesNotExist as ex:
                raise (Http404) from ex
        return attrs

class BoardSerializer(ModelSerializer):

    class Meta:
         model = Board
         fields = "__all__"

class BoardFullSerializer(ModelSerializer):
    threads = ThreadSerializer(many=True, read_only=True)

    class Meta:
         model = Board
         fields = ["slug", "verbose_name", "threads"]
