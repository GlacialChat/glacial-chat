from Chat.admin import admin_site
from .models import ChatLog, FileLog
from django.contrib.admin import ModelAdmin


class ChatLogAdmin(ModelAdmin):
    list_display = ('user', 'msg', 'pub_date')


class FileLogAdmin(ModelAdmin):
    list_display = ('user', 'f_name', 'pub_date')

admin_site.register(ChatLog, ChatLogAdmin)
admin_site.register(FileLog, FileLogAdmin)
