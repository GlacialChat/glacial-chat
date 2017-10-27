from django.db import models
from django.utils import timezone


class ChatMono(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    pub_date = models.DateTimeField('date published')
