from django.conf.urls import url

from apps.user_private.views import firstPageView,todayView,registerView,LoginView,ActiveView,tmrwView,pickStarView,logoutView
from apps.user_private.tests import dataTest

app_name = 'user_private'
urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^register$', registerView.as_view(), name='register'),
    url(r'^firstPage$', firstPageView.as_view(), name='firstPage'), # 登录
    url(r'^logout$', logoutView.as_view(), name='logout'),

    # 需要登录才能访问的：今日 & 明日 界面
    url(r'^today$', todayView.as_view(), name='today'),
    url(r'^tomorrow$', tmrwView.as_view(), name='tomorrow'),
    url(r'^pickStar$',pickStarView.as_view(),name='pickStar'),


    # 其它操作
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^dataTest$',dataTest,name='dataTest'),
]