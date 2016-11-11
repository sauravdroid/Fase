from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.user_register, name='register'),
    url(r'^returnurl', views.citrus_return_url, name='return_urlpyth'),
    url(r'^billgenerator', views.citrus_bill_generator, name='bill_generator'),
]
