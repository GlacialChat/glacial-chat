from Chat.admin import admin_site
from .models import ChatLog
from django.contrib.admin import ModelAdmin


class ChatLogAdmin(ModelAdmin):
    list_display = ('user', 'msg', 'pub_date')

admin_site.register(ChatLog, ChatLogAdmin)
