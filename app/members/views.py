from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# 장고 기본유저나 Custom유저모델 중, 사용중인 User모델을 가져옴
User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')
    return render(request, 'members/login.html')


def signup_view(request):
    """
    Template: index.html을 그대로 사용
        action만 이쪽으로
    URL: /members/signup/
    User에 name필드를 추가
        email,
        username,
        name,
        password
    를 전달받아, 새로운 User를 생성한다.
    생성시, User.objects.create_user() 메서드를 사용한다.
    이미 존재하는 username또는 email을 입력한 경우 "이미 사용중인 username/email입니다"라는 메시지를  HttpResponse로 돌려준다.
    생성에 성공하면 로그인 처리 후 (위의 login_view를 참조) posts:post-list로 redirect처리
    """
    # 사용자한테 입력받은 값
    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']

    if User.objects.filter(username=username).exists():
        return HttpResponse('이미 사용중인 username입니다.')
    if User.objects.filter(email=email).exists():
        return HttpResponse('이미 사용중인 email입니다.')

    user = User.objects.create_user(
        user=username,
        email=email,
        name=name,
        password=password,
    )
    login(request, user)
    return redirect('posts:post-list')


def logout_view(request):
    """
    GET요청으로 처리함
    요청에 있는 사용자를 logout처리
    djaong.contrib.auth.logout함수를 사용한다.

    URL: /members/logout/
    Template: 없음
   """
    logout(request)
    return redirect('members:login')
