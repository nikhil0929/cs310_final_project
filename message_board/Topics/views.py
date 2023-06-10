from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import json

from Topics.models import Topic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
    

# Gets list of all the topics and returns JSON list of topics
def list_topics(request):
    topic_list = Topic.objects.all()
    json_res = {
        "topics": list(topic_list.values("id", "name", "description"))
    }
    return JsonResponse(json_res)

# # show all topics that a user has not subscribed to
@csrf_exempt
@login_required
def list_unsubscribed_topics(request):
    if request.user.is_authenticated:
        user = request.user
        topic_list = Topic.objects.exclude(subscribers=user)
        json_res = {
            "topics": list(topic_list.values("id", "name", "description"))
        }
        return JsonResponse(json_res)
    else:
        return HttpResponse("You must be logged in to view this page", status=401)


@csrf_exempt
@login_required
def list_subscribed_topics(request):
    if request.user.is_authenticated:
        user = request.user
        topic_list = Topic.objects.filter(subscribers=user)
        json_res = {
            "topics": list(topic_list.values("id", "name", "description"))
        }
        return JsonResponse(json_res)
    else:
        return HttpResponse("You must be logged in to view this page", status=401)


# path('<int:topic_id>/subscribe/', views.subscribe_topic, name='topic_subscribe'),
@csrf_exempt
@login_required
def subscribe_topic(request, topic_id):
    if request.user.is_authenticated:
        user = request.user
        try:
            topic = Topic.objects.get(pk=topic_id)
            topic.subscribers.add(user)
            json_res = {
                "topic": {
                    "id": topic.id,
                    "name": topic.name,
                    "description": topic.description,
                    "subscriber_count": topic.subscribers.count(),
                }
            }
            return JsonResponse(json_res)
        except Topic.DoesNotExist:
            return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")
    else:
        return HttpResponse("You must be logged in to view this page", status=401)

def get_topic_detail(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        json_res = {
            "topic": {
                "id": topic.id,
                "name": topic.name,
                "description": topic.description,
                "subscriber_count": topic.subscribers.count(),
            }
        }
        return JsonResponse(json_res)
    except Topic.DoesNotExist:
        return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")

# TODO: Remove this decorator and implement authentication. Only authenticated users should be able to create topics
@csrf_exempt
def create_topic(request):
    if request.method == "POST":
        data = json.loads(request.body)

        my_name = data.get("name")
        my_description = data.get("description")
        
        name = my_name
        description = my_description
        topic = Topic.objects.create(name=name, description=description)
        json_res = {
            "topic": {
                "id": topic.id,
                "name": topic.name,
                "description": topic.description,
                "subscriber_count": topic.subscribers.count(),
            }
        }
        return JsonResponse(json_res)
    else:
        return HttpResponse("Only POST requests allowed", status=405)

# TODO: Remove this decorator and implement authentication. Only authenticated users should be able to update topics
@csrf_exempt
def update_topic(request, topic_id):
    if request.method == "PUT":
        try:
            topic = Topic.objects.get(pk=topic_id)

            '''
            YOU CANT USE THE FOLLOWING CODE TO RETRIEVE THE DATA FROM THE REQUEST

            When Django receives a PUT request, the data doesn't get populated in the request.POST dictionary like it does with a POST request. Instead, you should read the raw data from the request body and parse it manually.

            Sending Form data is not a conventional way of handling PUT requests. The more standard approach is to use PUT to handle JSON payloads.
            '''
            # DOES NOT WORK !!!
            # name = request.POST.get("name")
            # description = request.POST.get("description")

            data = json.loads(request.body)

            name = data.get("name")
            description = data.get("description")


            print(name, description)

            if name:
                topic.name = name

            if description:
                topic.description = description

            topic.save()

            json_res = {
                "topic": {
                    "id": topic.id,
                    "name": topic.name,
                    "description": topic.description,
                    "subscriber_count": topic.subscribers.count(),
                }
            }
            return JsonResponse(json_res)
        except Topic.DoesNotExist:
            return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")

# TODO: Remove this decorator and implement authentication. Only authenticated users should be able to delete topics
@csrf_exempt
def delete_topic(request, topic_id):
    if request.method == "DELETE":
        try:
            topic = Topic.objects.get(pk=topic_id)
            topic.delete()
            return HttpResponse(status=204)
        except Topic.DoesNotExist:
            return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")
        

# TODO: Remove this decorator and implement authentication. Only authenticated users should be able to subscribe to topics. THIS FUNCTION IS NOT TESTED BECAUSE I HAVE NOT IMPLEMENTED AUTHENTICATION YET
@csrf_exempt
def subscribe_topic(request, topic_id):
    if request.method == "POST":
        try:
            topic = Topic.objects.get(pk=topic_id)
            '''
            In Django, when a user is authenticated, their user object is automatically added to the request object as request.user. This is done using Django's authentication middleware, so you don't have to manually retrieve the user object in your view functions. 

            That's why in your function you can simply do topic.subscribers.add(request.user) without having to retrieve the user object.
            '''
            topic.subscribers.add(request.user)
            json_res = {
                "topic": {
                    "id": topic.id,
                    "name": topic.name,
                    "description": topic.description,
                    "subscriber_count": topic.subscribers.count(),
                }
            }
            return JsonResponse(json_res)
        except Topic.DoesNotExist:
            return HttpResponseNotFound(f"Topic with id {topic_id} does not exist")
    else:
        return HttpResponse("Only POST requests allowed", status=405)

