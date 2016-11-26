from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.UserRegistration.as_view(), name='register'),
    url(r'^seller_register$', views.seller_register, name='seller_register'),
    url(r'^set_favorite$', views.setFavoriteShop, name='set_favoriteshop'),
    url(r'^myfavoriteshops$', views.favshop.getFavoriteShop, name='get_favoriteshop'),
    url(r'^returnurl', views.citrus_return_url, name='return_urlpyth'),
    url(r'^billgenerator', views.citrus_bill_generator, name='bill_generator'),
    url(r'^create-app/$', views.create_app_api, name='create-app'),
    url(r'^check-app/$', views.check_app_api, name='check-app'),
    url(r'^create-app-web/$', views.create_app, name='create-app-web'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
