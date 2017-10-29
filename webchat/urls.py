from django.conf.urls import url, include
from . import views, admin

app_name = 'webchat'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'manage/', admin.admin_site.urls),
]