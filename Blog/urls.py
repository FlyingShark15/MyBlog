

from django.urls import path
from Blog.views import *


urlpatterns = [
    # 和前台相关的
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('tag/', tag, name='tag'),
    path('category/', category, name='category'),
    path('article/', article, name='article'),
    # path('error/', error, name='error'),
]
