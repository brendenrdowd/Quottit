from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^add$',views.add),
    url(r'^favorite/(?P<number>\d+)$',views.favorite),
    url(r'^user/(?P<number>\d+)$', views.display), #do i need the number?
    url(r'^remove/(?P<number>\d+)$',views.remove),
]
