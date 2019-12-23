from django.db import models


class Post(models.Model):
    '''
    인스타그램의 포스팅
    '''
    author =
    content =
    like_users = 'PostLike를 통한 Many-to-many구현'
    created =
    pass


class PostImage(models.Model):
    '''
    각 포스트의 사진
    '''
    pass


class PostComment(models.Model):
    '''
    각 포스트의 댓글 (Many-to-Many)
    '''
    pass


class PostLike(models.Model):
    '''
    사용자가 좋아요 누른 Post정보를 저장
    Many-to-Many필드를 중간모델(Intermediate Model)을 거쳐 사용
    언제 생성되었는지를 Extra fielf로 저장! (created)
    '''
