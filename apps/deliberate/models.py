from django.db import models

# Create your models here.
class deliberate(models.Model):
    # 设计字段
    # id + 对应用户id + 三省问题内容 + 问题创建日期
    user_id = models.IntegerField(verbose_name='关联用户id')
    type = models.TextField(verbose_name='问题')
    create_time = models.DateField(verbose_name='创建时间')

    class Meta:
        db_table = 'deliberate'
        verbose_name = '日省·问题'
        verbose_name_plural = verbose_name


class dlbr_answer(models.Model):
    # 设计字段
    # id + 对应问题id(fk) + 对应用户id + 回答内容 + 回答日期

    dlbr = models.ForeignKey(to="deliberate",on_delete=models.CASCADE,related_name='dlbr_answer')
    user_id = models.IntegerField(verbose_name='关联用户id')
    ans = models.TextField(verbose_name='回答内容')
    ans_time = models.DateField(verbose_name='回答日期')

    class Meta:
        db_table = 'dlbr_answer'
        verbose_name = '日省·回答'
        verbose_name_plural = verbose_name