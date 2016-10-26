from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'company'

urlpatterns = [
    url(r'^$', views.StockList.as_view(), name='api')
]
urlpatterns = format_suffix_patterns(urlpatterns)
