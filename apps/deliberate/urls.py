from django.conf.urls import url
from apps.deliberate.views import dlbr_detailView

app_name = 'deliberate'
urlpatterns = [
    url(r'^dlbr_detail$', dlbr_detailView.as_view(), name='dlbr_detail')
]