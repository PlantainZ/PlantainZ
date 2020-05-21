from django.db import models
# Create your models here.
# 计划表
class plan_finish(models.Model):
    user_id = models.IntegerField(verbose_name='用户id')
    date = models.DateField(verbose_name='完成日期')
    plan_id = models.IntegerField(verbose_name='项目id')

    finish_cpt = models.IntegerField(verbose_name='最新完成章', null=True)
    finish_sct = models.IntegerField(verbose_name='最新完成节', null=True)
    today_comment = models.TextField(verbose_name='今日评注',null=True)
    class Meta:
        db_table = 'plan_finish'
        verbose_name = '计划完成记录'
        verbose_name_plural = verbose_name

class plan(models.Model):
    status_choices = (
        (0, '提早'),
        (1, '正常'),
        (2, '延迟'),
    )
    user_id = models.IntegerField(verbose_name='关联用户id')
    decor_name = models.CharField(verbose_name='艺名',max_length=100)
    start_time = models.DateField(verbose_name='开始时间')
    end_time = models.DateField(verbose_name='结束时间')
    finish = models.SmallIntegerField(default=1,choices=status_choices,verbose_name='如何完成')
    is_firing = models.BooleanField(default=0,verbose_name='是否启动')
    type = models.TextField(verbose_name='分类')

    important = models.IntegerField(default=0,verbose_name='重要程度')
    hurry = models.IntegerField(default=0,verbose_name='紧急程度')


    class Meta:
        db_table = 'plan'
        verbose_name = '计划'
        verbose_name_plural = verbose_name

# 计划小节表
class plan_section(models.Model):
    user_id = models.IntegerField(verbose_name='关联用户id')
    pj_id=models.IntegerField(verbose_name='关联项目id')
    pj_name = models.TextField(verbose_name='关联项目名')
    chapter = models.IntegerField(verbose_name='单元号')
    section = models.IntegerField(verbose_name='小节号')
    title = models.TextField(verbose_name='任务标题')
    detail = models.TextField(verbose_name='任务详细')
    hover_tips = models.TextField(verbose_name='鼠标悬停提示')

    is_finished = models.BooleanField(verbose_name='是否已经完成',default=0)
    review_times = models.IntegerField(verbose_name='复盘次数',default=0)
    class Meta:
        db_table = 'plan_section'
        verbose_name = '计划细节'
        verbose_name_plural = verbose_name