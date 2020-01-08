from django.shortcuts import render, redirect
from .models import Post, PostLike


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


def post_like(request, pk):
    """
    pk가 pk인 Post와 (변수명 post사용)
    request.user로 전달되는 User (변수명 user사용)에 대해

    1. PostLike(post=post, user=user)인 PostLike객체가 존재하는지 확인한다.
    2-1. 만약 해당 객체가 이미 있다면, 삭제한다.
    2-2. 만약 해당 객체가 없다면 새로 만든다.
    3. 완료 후 posts:post-list로 redirect한다.
    """
    # pk로 Post를 가져오기
    #  Post.objects.get(키=값)

    # PostLike객체가 있는지 검사하기
    #  검색어: Django queryset exists
    #  PostLike.objects.filter(키1=값1, 키2=값2).exists()

    # 삭제하기
    #  PostLike.objects.filter(조건).delete()

    # redirect
    #  return redirect(URL name)

    post = Post.objects.get(pk=pk)
    user = request.user

    post_like_qs = PostLike.objects.filter(post=post, user=user)
    if post_like_qs.exists():
        post_like_qs.delete()
    else:
        PostLike.objects.create(post=post, user=user)

    return redirect('posts:post-list')


