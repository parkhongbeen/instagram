from django.shortcuts import render, redirect

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, PostLike, PostImage


def post_list(request, tag=None):
    # 1. 로그인 완료 후 이 페이지로 이동하도록 함
    # 2. index에 접근할 때 로그인이 되어 있다면, 이 페이지로 이동하도록 함
    #    로그인이 되어있는지 확인:
    #       User.is_authenticated가 True인지 체크
    #
    # URL:      /posts/ (posts.urls을 사용, config.urls에서 include)
    # Template: templates/posts/post-list.html
    #           <h1>Post List</h1>
    if tag is None:
        posts = Post.objects.order_by('-pk')
    else:
        posts = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')

    comment_form = CommentCreateForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post-list.html', context)


def post_list_by_tag(request, tag):
    # URL: /explore/tags/<tag문자열>/
    # Templates: /posts/post-list.html
    # <tag문자열>인 Tag를 자신(post).tags에 가지고 있는 경우인 Post목록만 돌려줘야 함
    # 이 내용 외에는 위의 post_list와 내용 동일
    posts = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')
    comment_form = CommentCreateForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
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


def post_create(request):
    """
       URL:        /posts/create/, name='post-create'
       Template:   /posts/post-create.html
       forms.PostCreateForm을 사용
       """
    if request.method == 'POST':
        # 새 Post를 생성
        # user는 request.user
        # 전달받는 데이터: image, text
        #  image는 request.FILES에 있음
        #  text는  request.POST에 있음

        # Post를 생성 (변수명 post를 사용)
        #   request.user와 text를 사용
        # PostImage를 생성
        #   post와 전달받은 image를 사용
        # 모든 생성이 완료되면 posts:post-list로 redirect
        text = request.POST['text']
        images = request.FILES.getlist('image')

        post = Post.objects.create(
            author=request.user,
            content=text
        )
        for image in images:
            post.postimage_set.create(image=image)

        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post-create.html', context)


def comment_create(request, post_pk):
    # URL: /posts/<int:post_pk>/comments/create/
    # Template: 없음(post-list.html내에 Form을 구현)
    # post-list.html 내부에서 각 post마다 자신에게 연결된 Postcommetn목록을 보여주도록 함
    #   보여주는 형식은
    #     <li><b>작성자명</b> <span>내용</span></li>
    #     <li><b>작성자명</b> <span>내용</span></li>
    # Form: post.forms.CommentCreateForm
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        # Form인스턴스를 만드는데, data에 request.POST로 전달된 dict를 입력
        form = CommentCreateForm(data=request.POST)
        # Form인스턴스 생성시, 주어진 데이터가
        # 해당 Form이 가진  Field들에 적절한 데이터인지 검증
        if form.is_valid():
            form.save(post=post, author=request.user)
        return redirect('posts:post-list')
