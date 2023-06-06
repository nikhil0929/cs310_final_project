from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    subscribers = models.ManyToManyField(User, related_name='subscribed_topics')

    def __str__(self):
        return self.name