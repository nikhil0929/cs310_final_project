from django.db import models
from django.contrib.auth.models import User
# import Topic 

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_topic = models.ForeignKey('Topics.Topic', on_delete=models.CASCADE, null=True, blank=True, related_name='topic_messages')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_messages')

    def __str__(self):
        return self.content[:50]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'message')

    def __str__(self):
        return f'{self.user.username} likes {self.message.content[:20]}'
