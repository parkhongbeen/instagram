from rest_framework import serializers

from members.serializers import UserSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'content',
            'postimage_set',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostSerializer(instance).data
