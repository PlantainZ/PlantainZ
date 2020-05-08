import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.urls import reverse
from .models import user_private
import os
import PlantainZ.settings as settings
import datetime
from django.contrib.auth.hashers import make_password,check_password # Django的数据库密码加密问题
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from celery_tasks.tasks import send_register_active_email
from utils.mixin import LoginRequiredMixin

#设置保存头像的路径
path = os.path.join(os.path.join(settings.BASE_DIR, "static"), "user_img_tmp")

class LoginView(View):
    def get(self,request):
            # 判断是否已经记录了用户名
            if 'username' in request.COOKIES:
                username = request.COOKIES.get('username')
                checked = 'checked'
            else:
                username = ''
                checked = ''

            # 使用模板
            return render(request, 'Season_01/01_login2.html', {'username': username, 'checked': checked})
            # 后面字典是传参进去。在template里面，
            # 有{{username}}这样的参数~就从这里传出去的

    def post(self, request):
        """使用django内置的认证系统来处理认证和login后的记录登录状态到session"""

        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')

        # 参数验证
        if not all([username, password]):
            # 参数不完整
            return render(request, 'Season_01/01_login2.html', {'errmsg': '数据不完整'})

        # 业务处理：用户注册，验证用户是否存在
        # 业务处理:登录校验
        # 有空参见dj文档~套用的而已~
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:  # 用户已激活
                # 记录用户的登录状态
                login(request, user)  # 是login模块

                # 默认跳转到首页
                # 如果获取到了next的值，就跳转到next值
                # 如果没有获取到，就跳转到firstPage页面。
                # reverse()是反向解析。
                next_url = request.GET.get('next', reverse('user_private:firstPage'))

                # 跳转到next_url
                response = redirect(next_url)
                # redirect返回的通常是HttpResponseRedirect对象

                # ==================================
                # 如果有session，并且是默认的，那么
                # 它就会保存在dj的数据库里面（读取很慢
                # 所以我们才需要有redis保存我们的参数数据库
                # ==================================
                # 判断是否需要记住用户名
                if remember == 'on':
                    # 记住用户名,为了这个功能，改过headers.py的__bytes__()，见书签
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'Season_01/01_login2.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'Season_01/01_login2.html', {'errmsg': '用户名或密码错误'})


class firstPageView(View):
    def get(self,request):
        # return render(request, 'mine/login.html')
        return render(request, 'Season_01/03_firstPage.html')

    def post(self,request):
        if self.request.is_ajax:
            username = request.POST.get('username')
            password = request.POST.get('pwd')

            db_user = user_private.objects.get(username = username)
            # db_user =authenticate(request,username, password)

            if check_password(password,db_user.password,setter='pbkdf2_sha256'):
            # if db_user is not None:
                # ajax是横在浏览器和服务器之间，注定无法进行重定向。
                # login(request, db_user)

                result = {"status":"redirect"}
                return HttpResponse(json.dumps(result))
            else:
                result = {"status": "错误"}
                return HttpResponse(json.dumps(result))
        else:
            pass

class registerView(View):
    def get(self,request):
        return  render(request, 'Season_01/02_register.html')

    def post(self,request):
        if self.request.is_ajax:
            username = request.POST.get("username")
            pwd = request.POST.get("password")
            email = request.POST.get("email")
            file_obj = request.FILES.get("avatar")
            file_name=''

            # 3.业务处理：用户注册，验证用户是否存在
            try:
                # 用户已经存在。这里的User.objects是调用DJ内部自带的User系统~
                user = user_private.objects.get(username=username)  # 注意最后会返回一个user对象
            except user_private.DoesNotExist:
                # 用户名不存在可以注册
                user = None
            if user:
                return render(request, 'Season_01/02_register.html', {'errmsg': '用户已存在'})

            # 重置文件名
            # if file_obj is not None:


            # 检查图片文件
            file_type = file_obj.name.split('.')[-1]
            if file_type not in ['jpeg', 'jpg', 'png']:
                return HttpResponse('输入文件有误')
            try:
                db_file_name = "user_img_tmp/" + username +'.'+ file_type
                file_name = path + '/' + username+'.'+file_type
                with open(file_name, 'wb+') as f:
                    f.write(file_obj.read())
            except Exception as e:
                print(e)

            # 数据库录入操作
            # 密码被加密，看密码是否相同的方法：check_password(“password明文”,“password密文”)
            # 明文应当是用户输入的，密文应当来自数据库。已验证，可行~
            try:
                user = user_private.objects.create_user(username=username,email=email,password=pwd,
                                                        is_superuser = 1,is_staff=1,
                                                        is_active = 0,
                                                        date_joined = datetime.datetime.now(),
                                                        last_login = datetime.datetime.now(),
                                                        user_img = db_file_name)
                # user.is_superuser = 1  ← 也可以这样子录入数据。
                user.save()
            except Exception as e:
                return render(request, 'Season_01/02_register.html', {'errmsg': '用户注册失败，请重试'})

            # 4.设置激活链接/user/active/user_id======================================
            serializer = Serializer(settings.SECRET_KEY, 3600)
            # 前面的参数是要加密的信息(密钥)，这里是用的本项目settings.py的第一行的SECRET_KEY这个信息，上头有导入~~
            # 后面的代表是生命周期，以s为对象，这里是1h
            info = {'confirm': user.id}

            token = serializer.dumps(info).decode('utf8')
            # 返回的是加密后的信息！（也就是token这个变量的内容）
            # dumps()就是一个加密的操作
            # 对应解密操作叫serializer.loads(token)，还原字典信息。

            # 5.发送邮件,delay放到队列中
            # 函数在celery_task中。发出去的：ip/user/active/user_id
            send_register_active_email.delay(email, username, token)
            # 发送邮件
            # subject = '杯酒寸心：账户激活'
            # message = ''
            # sender = settings.EMAIL_FROM  # 记得要初始化django，不然会在这里报错
            # receiver = [email]
            # html_message = '<h1>%s, 谢谢注册杯酒寸心~</h1>请点击下面链接激活您的账户<br/>' \
            #                '<a href="http://127.0.0.1:8000/user/active/%s">' \
            #                     'http://127.0.0.1:8000/user/active/%s' \
            #                '</a>' % (username, token, token)
            #
            # try: # django内置的发邮件操作
            #     send_mail(subject,
            #               message,
            #               sender,
            #               receiver,
            #               html_message=html_message, fail_silently=False)
            #     # html_message是为了让上面的字变成html格式
            # except Exception as e:
            #     print(e)

            result = {'rst':'注册成功'}
            return HttpResponse(json.dumps(result))




#=================================================================================

            result = {"status": "哎呀注册按钮通了！！"}
            return HttpResponse(json.dumps(result))


class todayView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request, 'Season_01/04_today.html')
class tmrwView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'Season_01/05_tmrw.html')

class ActiveView(View):
    """用户激活"""
    def get(self, request, token):
        # token解密，获取用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token) # 获取token的原信息
            user_id = info['confirm']

            # 根据id更改数据库胡is_active
            user = user_private.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转登录页面。使用反向解析
            # static里面的都是死的，template里面的html才是活的！！
            return redirect(reverse('user_private:login'))

        except SignatureExpired as e:
            # 激活链接一过期
            return HttpResponse('激活链接已经过期')
            # 实际操作要给它返回一个提示页面，而不是字
