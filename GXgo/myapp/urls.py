from . import views
from django.urls import re_path
app_name ='[myapp]'
urlpatterns = [
    re_path('^index/$',views.index,name = 'index'),
    re_path('^regist/$',views.regist,name = 'regist'),
    re_path('^login/$',views.login,name = 'login'),
    re_path('^mine/(\d+)$',views.mine,name = 'mine'),
    re_path('^myorder/(\d+)$',views.myorder,name = 'myorder'),
    re_path('^quit/$',views.quit,name='quit'),
    re_path('^change/(\d+)/(\d+)$',views.change,name = 'change'),
    re_path('^islogin/$',views.isLogin,name = 'isLogin'),
    re_path('^verifycode/$',views.verifycode,name = 'verifycode'),
    re_path('^checkacc/$',views.checkacc,name='checkacc')
]
