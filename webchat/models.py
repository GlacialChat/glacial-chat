"""
Defines the models used in webchat
"""

from django.db import models
from django.contrib.auth.models import User


class ChatLog(models.Model):
    def msg(self):
        """
        :return: a formatted version of the message, containing at most 10 letters
        """
        return self.message[:7] + '...'

    # the publication date
    pub_date = models.DateTimeField("date published")

    # the OP of the ChatLog
    user = models.ForeignKey(User)

    # the message/content of the ChatLog
    message = models.TextField()


class FileLog(models.Model):
    def f_name(self):
        """
        :return: file's name
        """
        return self.file.name

    # the publication date
    pub_date = models.DateTimeField("date published")

    # the OP of the FileLog
    user = models.ForeignKey(User)

    # the file/content of the FileLog
    file = models.FileField()
