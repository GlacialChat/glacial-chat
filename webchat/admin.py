from django.contrib.admin import AdminSite


class WCAdminChat(AdminSite):
    site_header = "Web Chat"
    site_title = "Web Chat"

admin_site = WCAdminChat(name='wcadmin')
