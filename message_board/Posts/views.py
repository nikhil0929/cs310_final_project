from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from Topics.models import Topic
from .models import Message, Comment, Like


    # # List all main message posts under a specific topic.
    # path('topics/<int:topic_id>/messages/', views.message_list, name='message_list'),

    # # Get the message post detail for a specific message post under a topic.
    # path('topics/<int:topic_id>/messages/<int:message_id>/', views.message_detail, name='message_detail'),

    # # Create a new message under a specific topic.
    # path('topics/<int:topic_id>/messages/create/', views.message_create, name='message_create'),

    # # Update a specific message under a specific topic.
    # path('topics/<int:topic_id>/messages/<int:message_id>/update/', views.message_update, name='message_update'),

    # # Delete a specific message under a specific topic.
    # path('topics/<int:topic_id>/messages/<int:message_id>/delete/', views.message_delete, name='message_delete'),

    # # Add a comment to a specific message.
    # path('topics/<int:topic_id>/messages/<int:message_id>/comments/create/', views.comment_create, name='comment_create'),

    # # List all comments under a specific message.
    # path('topics/<int:topic_id>/messages/<int:message_id>/comments/', views.comment_list, name='comment_list'),

    # # Update a comment under a specific message.
    # path('topics/<int:topic_id>/messages/<int:message_id>/comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),

    # # Delete a comment under a specific message.
    # path('topics/<int:topic_id>/messages/<int:message_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # # Like a specific message or comment.
    # path('messages/<int:message_id>/like/', views.like_message, name='like_message'),

    # # Remove like from a specific message or comment.
    # path('messages/<int:message_id>/unlike/', views.unlike_message, name='unlike_message'),

@csrf_exempt
def message_list(request, topic_id):
    try:
        # The advantage of the below method is that it checks the existence of the Topic before trying to access its related Messages, which can be helpful for error handling.

        # Instead of:
        # all_messages = Message.objects.filter(parent_topic_id=topic_id)

        my_topic = Topic.objects.get(pk=topic_id)
        messages = my_topic.topic_messages.all()

        json_res = {
            "messages": list(messages.values("id","title", "content", "created_at", "parent_topic_id", "author__username"))
        }
        return JsonResponse(json_res)
    except Topic.DoesNotExist:
        return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")

@csrf_exempt
def message_detail(request, topic_id, message_id):
    try:
        msg = Message.objects.get(pk=message_id, parent_topic_id=topic_id)
        json_res = {
            "message": {
                "id": msg.id,
                "title" : msg.title,
                "content": msg.content,
                "created_at": msg.created_at,
                "topic_id": msg.parent_topic_id,
                "author": msg.author.username
            }
        }
        return JsonResponse(json_res)
    except Message.DoesNotExist:
        return HttpResponseNotFound(f"Message with id {message_id} under Topic {topic_id} does not exist")

@login_required
@csrf_exempt
def message_create(request, topic_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            my_title = data.get("title")
            my_content = data.get("content")
            
            topic = Topic.objects.get(pk=topic_id)
            msg = Message.objects.create(
                title=my_title,
                content=my_content,
                parent_topic=topic,
                author=request.user
            )
            json_res = {
                "message": {
                    "id": msg.id,
                    "title" : msg.title,
                    "content": msg.content,
                    "created_at": msg.created_at,
                    "topic_id": msg.parent_topic_id,
                    "author": msg.author.username
                }
            }
            return JsonResponse(json_res, status=200)
        except Topic.DoesNotExist:
            return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")
    else:
        return HttpResponse("Only POST requests are allowed", status=405)

@login_required
@csrf_exempt
def message_update(request, topic_id, message_id):
    if request.method == "PUT":
        try:
            
            msg = Message.objects.get(pk=message_id, parent_topic_id=topic_id)

            if request.user.id != msg.author.id:
                return HttpResponse("You are only allowed to update your own message!", status=403)

            body = json.loads(request.body)
            new_content = body.get("content")
            new_title = body.get("title")

            if new_content:
                msg.content = new_content
            if new_title:
                msg.title = new_title

            msg.save()
            json_res = {
                "message": {
                    "id": msg.id,
                    "title" : msg.title,
                    "content": msg.content,
                    "updated_at": msg.updated_at,
                    "topic_id": msg.parent_topic_id,
                    "author": msg.author.username
                }
            }
            return JsonResponse(json_res, status=200)
        except Message.DoesNotExist:
            return HttpResponseNotFound(f"Message with id {message_id} under Topic {topic_id} does not exist")

@login_required
@csrf_exempt
def message_delete(request, topic_id, message_id):
    if request.method == "DELETE":
        try:
            msg = Message.objects.get(pk=message_id, parent_topic_id=topic_id)
            if request.user.id != msg.author.id:
                return HttpResponse("You cannot delete other users messages!", status=403)
            msg.delete()
            return HttpResponse("Message deleted successfully", status=204)
        except Message.DoesNotExist:
            return HttpResponseNotFound(f"Message with id {message_id} under Topic {topic_id} does not exist")

@login_required
@csrf_exempt
def comment_create(request, topic_id, message_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            my_content = data.get("content")
            msg = Message.objects.get(pk=message_id, parent_topic_id=topic_id)
            comment = Comment.objects.create(
                content=my_content,
                parent_message=msg,
                author=request.user
            )
            json_res = {
                "comment": {
                    "id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "message_id": comment.parent_message_id,
                    "author": comment.author.username
                }
            }
            return JsonResponse(json_res, status=201)
        except Message.DoesNotExist:
            return HttpResponseNotFound(f"Message with id {message_id} under Topic {topic_id} does not exist")

@csrf_exempt
def comment_list(request, topic_id, message_id):
    try:
        msg = Message.objects.get(pk=message_id, parent_topic_id=topic_id)
        comments = msg.comments.all()
        json_res = {
            "comments": list(comments.values("id", "content", "created_at", "parent_message_id", "author__username"))
        }
        return JsonResponse(json_res)
    except Message.DoesNotExist:
        return HttpResponseNotFound(f"Message with id {message_id} under Topic {topic_id} does not exist")

@login_required
@csrf_exempt
def comment_update(request, topic_id, message_id, comment_id):
    if request.method == "PUT":
        try:
            comment = Comment.objects.get(pk=comment_id, parent_message_id=message_id)

            if request.user.id != comment.author.id:
                return HttpResponse("You are only allowed to update your own comment!", status=403)
            
            body = json.loads(request.body)
            new_content = body.get("content")
            if new_content:
                comment.content = new_content
            comment.save()
            json_res = {
                "comment": {
                    "id": comment.id,
                    "content": comment.content,
                    "updated_at": comment.updated_at,
                    "message_id": comment.parent_message_id,
                    "author": comment.author.username
                }
            }
            return JsonResponse(json_res)
        except Comment.DoesNotExist:
            return HttpResponseNotFound(f"Comment with id {comment_id} under Message {message_id} does not exist")

@login_required
@csrf_exempt
def comment_delete(request, topic_id, message_id, comment_id):
    if request.method == "DELETE":
        try:
            comment = Comment.objects.get(pk=comment_id, parent_message_id=message_id)
            if request.user.id != comment.author.id:
                return HttpResponse("You cannot delete other users comments!", status=403)
            comment.delete()
            return HttpResponse(status=204)
        except Comment.DoesNotExist:
            return HttpResponseNotFound(f"Comment with id {comment_id} under Message {message_id} does not exist")

@login_required
@csrf_exempt
def like_message(request, message_id):
    if request.method == "POST":
        try:
            message = Message.objects.get(pk=message_id)
            
            # Check if the like already exists
            if Like.objects.filter(user=request.user, message=message).exists():
                return HttpResponse("You have already liked this message", status=400)

            # Create the like
            Like.objects.create(user=request.user, message=message)
            
            return HttpResponse("Message liked successfully")

        except Message.DoesNotExist:
            return HttpResponseNotFound(f"Message with id {message_id} does not exist")

    else:
        return HttpResponse("Only POST requests allowed", status=405)
    

@login_required
@csrf_exempt
def unlike_message(request, message_id):
    if request.method == "DELETE":
        try:
            message = Message.objects.get(pk=message_id)

            # Check if the like exists
            like = Like.objects.filter(user=request.user, message=message).first()
            if like is None:
                return HttpResponse("You have not liked this message", status=400)

            # Delete the like
            like.delete()

            return HttpResponse("Like removed successfully")

        except Message.DoesNotExist:
            return HttpResponseNotFound(f"Message with id {message_id} does not exist")
    else:
        return HttpResponse("Only DELETE requests allowed", status=405)



