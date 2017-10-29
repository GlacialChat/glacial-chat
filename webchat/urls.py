from django.conf.urls import url
from . import views, admin

app_name = 'webchat'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'manage/', admin.admin_site.urls),
]