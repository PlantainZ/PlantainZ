from django.conf.urls import url

from apps.plan.views import pickStarView,daySwitchView
from apps.plan.tests import dataTest

app_name = 'plan'
urlpatterns = [
    url(r'^pickStar$', pickStarView.as_view(), name='pickStar'),
    url(r'^daySwitch$', daySwitchView.as_view(), name='daySwitch'),
]