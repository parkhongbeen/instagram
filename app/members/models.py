from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField('프포필이미지', blank=True, upload_to='users/')
