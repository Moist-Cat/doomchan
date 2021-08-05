from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
#from rest_framework.relations import PrimaryKeyRelatedField
from ..models import Board, Thread, Comment

class BoardSerializer(ModelSerializer):

    class Meta:
         model = Board
         fields = '__all__'

class ThreadSerializer(ModelSerializer):

    class Meta:
         model = Thread
         fields = '__all__'

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['name', 'comment', 'thread', 'image', 'active']

class ThreadFullSerializer(ThreadSerializer):
    comments = CommentSerializer(many=True, read_only=True)
"""
    class Meta:
         model = Thread
         fields = ['comments']
"""
        
