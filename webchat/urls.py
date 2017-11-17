"""
urls.py for webchat application / root application
all views are stored in 'webchat/views.py'

root/index: '/'            => Index view
success:    '/success/'    => Success view
transcript: '/transcript/' => Transcript view
files:      '/files/'      => Files view
"""

from django.conf.urls import url

from . import views


app_name = 'webchat'

urlpatterns = [
    # index view, using index.html
    url(r'^$', views.Index.as_view(), name='index'),
    # success view, using success.html
    url(r'success/$', views.Success.as_view(), name='success'),
    # transcript view, using transcript.html
    url(r'transcript/$', views.Transcript.as_view(), name='transcript'),
    # files view, using files.html
    url(r'files/$', views.Files.as_view(), name='files'),
]
