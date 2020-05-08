from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """登录状态判断的扩展类"""

    @classmethod # 表明是自己的方法，
    def as_view(cls, **initkwargs):
        # 调用父类的as_view，生成
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)