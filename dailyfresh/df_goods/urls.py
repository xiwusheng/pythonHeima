from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.good_list, name="good_list"),
    url(r'^(\d+)/$', views.detail, name="detail"),

]