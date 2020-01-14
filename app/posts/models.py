import re

from django.db import models

from members.models import User


class Post(models.Model):
    TAG_PATTERN = re.compile(r'#(\w+)')
    """
    인스타그램의 포스팅
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    like_users = models.ManyToManyField(User, through='PostLike', related_name='like_post_set')
    # author, like_users 각 각에 있는 user가 충돌나지않게 related_name을 사용
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        'Tag', verbose_name='해시태그 목록', related_name='posts', blank=True
    )

    def __str__(self):
        return '{author} | {created}'.format(
            author=self.author.username,
            created=self.created,
        )

    def _save_html(self):
        self.content_html = re.sub(
            self.TAG_PATTERN,
            r'<a href="/explore/tags/\g<1>/">#\g<1></a>',
            self.content,
        )

    def _save_tags(self):
        tag_name_list = re.findall(self.TAG_PATTERN, self.content)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_name_list]
        self.tags.set(tags)

        # 자신의 content_html에
        # #Python -> <a href="/explore/tags/Python/>#Python</a>
        # 로 변환된 문자열을 저장

        # Post객체가 저장될 때, content값을 분석해서
        # 자신의 tags항목을 적절히 채워줌
        # ex) #Django #python이 온 경우
        #     post.tags.all()시
        #      name이 Django, python인 Tag 2개 QuerySet이 리턴되어야 함

    def save(self, *args, **kwargs):
        self._save_html()
        super().save(*args, **kwargs)
        self._save_tags()


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


class Tag(models.Model):
    """
    HashTag의 Tag를 담당
    Post입장에서 post.tags.all()로 연결된 전체  Tag전체를 불러올 수 있어야 함
    Tag입장에서 tag.posts.all()로 연결된 전체 Post를 불러올 수 있어야 함

    Django admin에서 결과를 볼 수 있도록  admin.py에 적절히 내용 기록
    중개모델 (Intermediate model)을 사용할 필요 없음
    """
    name = models.CharField('태그명', max_length=100)

    def __str__(self):
        return self.name
