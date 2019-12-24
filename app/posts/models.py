from django.db import models

from members.models import User


class Post(models.Model):
    """
    인스타그램의 포스팅
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_users = models.ManyToManyField(User, through='PostLike', related_name='like_posts_set')
    # author, like_users 각 각에 있는 user가 충돌나지않게 related_name을 사용
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{author} | {created}'.format(
            author=self.author.username,
            created=self.created,
        )


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
