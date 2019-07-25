# coding=utf-8
"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


from django.views.static import serve  # 上传文件处理函数
from .settings import MEDIA_ROOT

urlpatterns = [
    # 此处不能提前配置,如果df_goods下没有urls.py的话
    url(r'^admin/', include(admin.site.urls)),

    url(r'^user/', include('df_user.urls', namespace='df_user')),
    url(r'^', include('df_goods.urls', namespace='df_goods')),
    url(r'^tinymce/', include('tinymce.urls')),  # 使用富文本编辑框配置confur1
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}), # 此处serve MEDIA_ROOT为了能够浏览器访问到
]


