from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# from db.BaseModel import BaseModel

# is_superuser: 是否管理员
# is_staff: 是否开发者
class user_private(AbstractUser):
    user_img = models.TextField(verbose_name='头像路径',default=None)
    class Meta:
        db_table = 'user_private'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
