from django.shortcuts import render
from .models import Post


def post_list(request):
    # 1. 로그인 완료 후 이 페이지로 이동하도록 함
    # 2. index에 접근할 때 로그인이 되어 있다면, 이 페이지로 이동하도록 함
    #    로그인이 되어있는지 확인:
    #       User.is_authenticated가 True인지 체크
    #
    # URL:      /posts/ (posts.urls을 사용, config.urls에서 include)
    # Template: templates/posts/post-list.html
    #           <h1>Post List</h1>
    posts = Post.objects.order_by('-pk')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post-list.html', context)
