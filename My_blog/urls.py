"""My_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.views import static


from Blog.upload import upload_image
'''
如果项目比较大，url比较多的话，即app多，不能全部写在这个工程项目中
否则很难去维护管理，所以在app，比如Bolg中加入一个urs.py，然后在这里引入
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    # 在这里加入前端页面的urls
    path('', include('Blog.urls')),
    # 配置上传图片功能
    # 这里的差异，https://blog.csdn.net/qq_40397452/article/details/80698014
    re_path('^uploads/(?P<path>.*)$', static.serve, {"document_root": settings.MEDIA_ROOT, }),
    re_path('^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image')
]
