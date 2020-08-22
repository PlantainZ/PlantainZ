from django.conf.urls import url

from apps.plan.views import pickStarView,daySwitchView,planAddView

app_name = 'plan'
urlpatterns = [
    url(r'^pickStar$', pickStarView.as_view(), name='pickStar'),
    url(r'^daySwitch$', daySwitchView.as_view(), name='daySwitch'),
    url(r'^planAdd$', planAddView.as_view(), name='planAdd'),
]