from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'module/(?P<id>\d+)$', views.get_module_by_id,),
    url(r'module/(?P<username>[-\w]+)$', views.get_module_by_username,),
    url(r'module/$', views.get_module_list,),
]