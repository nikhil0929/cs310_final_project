from django.urls import path

from . import views

urlpatterns = [
    # List all main message posts under a specific topic.
    path('topics/<int:topic_id>/messages/', views.message_list, name='message_list'),

    # Get the message post detail for a specific message post under a topic.
    path('topics/<int:topic_id>/messages/<int:message_id>/', views.message_detail, name='message_detail'),

    # Create a new message under a specific topic.
    path('topics/<int:topic_id>/messages/create/', views.message_create, name='message_create'),

    # Update a specific message under a specific topic.
    path('topics/<int:topic_id>/messages/<int:message_id>/update/', views.message_update, name='message_update'),

    # Delete a specific message under a specific topic.
    path('topics/<int:topic_id>/messages/<int:message_id>/delete/', views.message_delete, name='message_delete'),

    # Add a comment to a specific message.
    path('topics/<int:topic_id>/messages/<int:message_id>/comments/create/', views.comment_create, name='comment_create'),

    # List all comments under a specific message.
    path('topics/<int:topic_id>/messages/<int:message_id>/comments/', views.comment_list, name='comment_list'),

    # Update a comment under a specific message.
    path('topics/<int:topic_id>/messages/<int:message_id>/comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),

    # Delete a comment under a specific message.
    path('topics/<int:topic_id>/messages/<int:message_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # Like a specific message or comment.
    path('messages/<int:message_id>/like/', views.like_message, name='like_message'),

    # Remove like from a specific message or comment.
    path('messages/<int:message_id>/unlike/', views.unlike_message, name='unlike_message'),
]

# print("i'm quitting school and becoming a gas station attendant")