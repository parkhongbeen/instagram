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
        """
        content에 포함된 해시태그 문자열 (ex: #python)의 Tag들을 만들고,
        자신의 tags Many-yomany field를 추가한다.
        """
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
    # postcomment_set <- related_name
    # 반대쪽 객체에서 사용
    # post.postcomment_set
    #
    # postcommnet <-related_query_name
    # 반대쪽 QuerySet의 filter조건 키워드명으로 사용
    # Post.objects.filter(postcommnet__)
    #
    # 기본값
    # related_name: <모델클래스명의 lowercase>_set
    # related_query_name: <모델클래스명의 lowercase>
    #
    # related_name을 지정하고, related_query_name은 지정하지 않은 경우
    # related_name: 지정한 related_name
    # related_query_name: 지정한 related_name
    # ex_ Post와 Tag관계(M2M)에서,  tags필드에서의 related_name이 posts인 경우
    # tag.posts.all() <-related_name
    # Tag.objects.filter(tags__) <-related_query_name

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
