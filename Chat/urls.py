"""
Chat URL Configuration

root: '/'        => webchat/urls.py                  # main site app / root site
site: '/manage/' => Chat/admin.py admin_site.urls    # administration site
"""

from django.conf.urls import url, include
from . import admin

urlpatterns = [
    url(r'^', include('webchat.urls')),
    url(r'^manage/', admin.admin_site.urls, name='admin'),
]
