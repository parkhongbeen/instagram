from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from posts.serializer import PostSerializer, PostCreateSerializer


class PostListCreateAPIView(APIView):
    """
    generics.ListCreateAPIView를 상속받아 동작하게 구현
    """

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class PostImageCreateAPIView(APIView):
    """
    PostImageCreateSerializer를 사용하도록 구현
    """

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getlist('image'):
            post.postimage_set.create(image=image)

        serializer = PostCreateSerializer(post)
        return Response(serializer.data)
