from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from posts.serializer import PostSerializer, PostCreateSerializer, PostCommentSerializer, PostCommentCreateSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostImageCreateAPIView(APIView):
    """
    PostImageCreateSerializer를 사용하도록 구현
    """

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getlist('image'):
            data = {'image': image}
            serializer = PostCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post)
            else:
                return Response(serializer.errors)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostCommentListCreateAPIView(APIView):
    # URL: /api/posts/1/comments/

    def get(self, request, post_pk):
        # post_pk에 해당하는 Post 에 연결된 PostComment 전체 가져오기
        # many=True
        post = get_object_or_404(Post, pk=post_pk)
        comments = post.postcomment_set.all()
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        # post_pk에 해당하는 Post 에 연결되는 PostComment 생성하기
        # content: request.data
        # author: request.user
        # post: URL params
        post = get_object_or_404(Post, pk=post_pk)
        serializer = PostCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
