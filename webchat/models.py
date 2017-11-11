from django.db import models
from django.contrib.auth.models import User


class ChatLog(models.Model):
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User)
    message = models.TextField()
