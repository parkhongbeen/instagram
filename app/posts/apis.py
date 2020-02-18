from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer
from posts.models import Post
from posts.serializer import PostSerializer


class PostListCreateAPIView(APIView):
    def get(self, request):
        return Response('aaa')
