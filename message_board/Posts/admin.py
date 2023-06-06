from django.contrib import admin

from Posts.models import Message
from Topics.models import Topic

admin.site.register(Topic)
admin.site.register(Message)
