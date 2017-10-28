from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatLog(models.Model):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.pub_date = timezone.now()
        obj.save()

    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User)
    message = models.TextField()
