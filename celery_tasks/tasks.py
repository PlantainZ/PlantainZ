from celery import Celery


from django.core.mail import send_mail # dj自带的发邮件东西
from django.template import loader

from PlantainZ import settings

"""
    关于celery的说明:
    1- 代码库-redis中间人-worker 可能并不是都在同一台计算机，但是worker的那一台计算机必须拥有代码库中的代码
    2- 代码库中的代码不需要加上下面的django初始化环境，因为runserver的时候就已经初始化好了，但是worker的那一台计算机必须加上django的环境环境初始化
    3- worker的那一台电脑，并不需要运行代码库，而是需要切换到代码目录下启动celery：celery -A celery_tasks.tasks worker -l info
    4- 代码库中当用户点击注册的时候使用delay()把任务加载到redis中， worker中监听8号库中的redis，有任务就去处理 
    5- 因为本次编写都在同一台电脑，所以加上下面的初始化代码
    6- 初始化django否则处理email的时候话读取不到settings下面的settings.EMAIL_FROM
"""

'''
下面四句，在任务发出者端并不需要
但是在任务处理者的一方就要!!
'''
# ===============================================
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PlantainZ.settings')
#这东西是从dailyfresh-wsgi.py的dj初始化文件那里复制来的！
#为了让下面需要初始化的地方不报错
django.setup() # 启动
# =================================================



# 任务发出者/中间人/处理者 可以在同一台电脑上启动，
# 也可以不在同一台电脑上。
# 但是每个涉及的环境都需要有celery！


# 创建一个celery对象,指定celery中间商的位置和第几号库，
# worker所在的电脑必须拥有相同的django代码才知道，如何链接redis和执行下面的代码
# 用户名密码的话，broker="redis://:password@127.0.0.1"
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379')
# 字符串是Celery对象的名字~改成其它也可以，不一定非要是路径
# broker是中间消息队列。
# 我们把任务塞进broker，然后Celery监听，有任务就及时接收。
# /8是第8号数据库。

# 装饰函数使用app
# 就tm离谱，为了让celery知道自己的代码，还得在远程的地方也有一份完整的代码
#
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""# to_email 是发给谁的意思

    # 发送邮件
    subject = '杯酒寸心：谢谢注册~'
    message = ''
    sender = settings.EMAIL_FROM # 记得要初始化django，不然会在这里报错
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您注册杯酒寸心</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)

    try:
        send_mail(subject,
                  message,
                  sender,
                  receiver,
                  html_message=html_message, fail_silently=False)
        # html_message是为了让上面的字变成html格式
    except Exception as e:
        print(e)

# # 类的导入写在celery配置完成的下方
# from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
#
# @app.task # 装饰器，给函数加上一些信息
# def generate_static_index_html():
#     """产生首页静态化页面"""
#
#     # 获取商品的种类信息
#     types = GoodsType.objects.all()
#
#     # 获取轮播图信息
#     banners = IndexGoodsBanner.objects.all().order_by('index')
#
#     # 获取促销信息
#     promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
#
#     # 获取首页分类商品展示信息
#     for type in types:
#         image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
#         title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
#
#         type.image_banners = image_banners
#         type.title_banners = title_banners
#
#     context = {
#         'types': types,
#         'goods_banners': banners,
#         'promotion_banners': promotion_banners,
#     }
#
#     # 产生静态界面
#     temp = loader.get_template('static_index.html')
#     static_index_html = temp.render(context)
#
#     save_path = os.path.join(settings.BASE_DIR, 'static/checkBox_index.html')
#
#     with open(save_path, 'w') as f:
#         f.write(static_index_html)
