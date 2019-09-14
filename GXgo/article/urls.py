from . import views
from django.urls import re_path
app_name ='[article]'
urlpatterns = [
    re_path('^test/(\d+)$',views.test,name = 'test'),
    re_path('^show/(\d+)/(\d+)$',views.show,name = 'show'),
    re_path('^delete/(\d+)$',views.delete,name = 'delete')
]
