from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.user_register, name='register'),
    url(r'^seller_register$', views.seller_register, name='seller_register'),
    url(r'^set_favorite$', views.setFavoriteShop, name='set_favoriteshop'),
    url(r'^myfavoriteshops$', views.favshop.getFavoriteShop, name='get_favoriteshop'),
    url(r'^returnurl', views.citrus_return_url, name='return_urlpyth'),
    url(r'^billgenerator', views.citrus_bill_generator, name='bill_generator'),
]

urlpatterns = format_suffix_patterns(urlpatterns)