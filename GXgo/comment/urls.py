from django.urls import re_path
from .import views

app_name = 'comments'

urlpatterns = [
    re_path('^post/(\d+)/(\d+)$',views.postCom,name='com'),
    re_path('^delete/(\d+)$',views.delete,name = 'del')
]