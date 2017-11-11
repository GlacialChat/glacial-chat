from django.conf.urls import url
from . import views


app_name = 'webchat'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'success/$', views.Success.as_view(), name='success'),
]
