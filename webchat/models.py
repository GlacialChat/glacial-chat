from django.db import models
from django.contrib.auth.models import User


class ChatLog(models.Model):
    def msg(self):
        return self.message[:10] + '...'

    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User)
    message = models.TextField()


class FileLog(models.Model):
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User)
    file = models.FileField()
