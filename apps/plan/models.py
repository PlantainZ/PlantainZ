from django.db import models
# Create your models here.
# 计划表

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


    # 关联外键：若plan_section有related_name，那就按照rn写，不要写_set
    # print(pub_obj.plan_section_set)  # 关系管理对象，与该出版社相关联的图书的关系，默认的书写方式：类名小写_set
    # print(pub_obj.plan_section_set.all())  # 所关联的所有的对象

    class Meta:
        db_table = 'plan'
        verbose_name = '计划'
        verbose_name_plural = verbose_name



# 计划小节表
class plan_section(models.Model):
    status_choices = (
        (0, '未完成'),
        (1, '正在进行'),
        (2, '完成'),
    )

    user_id = models.IntegerField(verbose_name='关联用户id')

    # pj_id=models.IntegerField(verbose_name='关联项目id')
    # pj_id 改成外键：
    pj = models.ForeignKey(to="plan",on_delete=models.CASCADE,related_name='plan_sections') # 最后加多了个's'
    # print(book.pub,type(book.pub))  # 会显示所关联的对象
    # print(book.pub_id,type(book.pub_id))  # 显示的是所关联的对象的pk
    # 新增：
    # models.Book.objects.create(title=title, pj=models.Publisher.objects.get(pk=xxx))
    # models.Book.objects.create(title=title, pj_id=xxx)
    # 输出外键属性：
    # print(book_obj.plan)  # book对象对应的外键对象
    # print(book_obj.plan.decor_name)  # 外键对象的name属性

    pj_name = models.TextField(verbose_name='关联项目名')
    chapter = models.IntegerField(verbose_name='单元号')
    section = models.IntegerField(verbose_name='小节号')
    title = models.TextField(verbose_name='任务标题')
    detail = models.TextField(verbose_name='任务详细')
    hover_tips = models.TextField(verbose_name='鼠标悬停提示')

    plan_status = models.BooleanField(verbose_name='任务状态', choices=status_choices,default=0)
    finish_start = models.DateTimeField(verbose_name='完成时间段：开始',null=True)
    finish_end = models.DateTimeField(verbose_name='完成时间段：结束',null=True)
    review_times = models.IntegerField(verbose_name='复盘次数', default=0)

    class Meta:
        db_table = 'plan_section'
        verbose_name = '计划细节'
        verbose_name_plural = verbose_name



class plan_comment(models.Model):
    # pj = models.ForeignKey(to="user_private", on_delete=models.CASCADE, related_name='plan_sections')
    user = models.ForeignKey(to = 'user_private.user_private',on_delete=models.CASCADE,related_name='user_id')
    # user_id = models.IntegerField(verbose_name='用户id')
    datetime = models.DateTimeField(verbose_name='日期')
    plan_id = models.IntegerField(verbose_name='项目id')

    cpt = models.IntegerField(verbose_name='章', null=True)
    sct = models.IntegerField(verbose_name='节', null=True)
    today_comment = models.TextField(verbose_name='评注',null=True)
    class Meta:
        db_table = 'plan_comment'
        verbose_name = '计划评论'
        verbose_name_plural = verbose_name