from django.contrib.admin import AdminSite
from .models import ChatLog

class WCAdminChat(AdminSite):
    site_header = "Web Chat"
    site_title = "Web Chat"


admin_site = WCAdminChat(name='wcadmin')
admin_site.register(ChatLog)
