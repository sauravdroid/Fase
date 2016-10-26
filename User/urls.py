from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.user_register, name='register'),
]
