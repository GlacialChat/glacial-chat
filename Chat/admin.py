from django.contrib.admin import AdminSite
from django.contrib.auth import admin


class WCAdminChat(AdminSite):
    site_header = "Glacial Chat"
    site_title = "Glacial Chat"
    index_title = "Manage Glacial Chat"


admin_site = WCAdminChat(name='wcadmin')
admin_site.register(admin.User)
admin_site.register(admin.Group)
