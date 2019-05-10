from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'module/user/(?P<pk>[-\w]+)', views.QureyModuleByUser.as_view(), ),
    url(r'module/user/(?P<pk>\d+)', views.QureyModule.as_view(), ),
    url(r'module/(?P<pk>\d+)', views.QureyModule.as_view(), ),
    url(r'module/$', views.QureyModule.as_view(), ),
    url(r'module/list$', views.QureyModuleList.as_view(), ),
    url(r'testScripts/mo/(?P<pk>\d+)$', views.QueryPressureTest.as_view(), ),
    url(r'testScripts/(?P<pk>\d+)$', views.PressureTestView.as_view()),
    url(r'testScripts/$', views.PressureTestView.as_view())
]