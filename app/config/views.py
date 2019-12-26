from django.shortcuts import render


def index(request):
    """
    settings.TEMPLATES의 DIRS에
        instagram/app/teplates 경로를 추가

    Template: templates/index.html
        <h1>INDEX!</h1>
    URL:        '/', name='index'

    bas.html추가
        상단 {% load static %}
        wjdwjrvkdlf qnffjdhf Eo {% static '경로' %}로 불러옴

    index.html과 login.html이 base.html을 extends하도록 함
    """
    return render(request, 'index.html')
