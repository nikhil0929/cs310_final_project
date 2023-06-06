from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_topics, name='topic_list'),
    path('<int:topic_id>/', views.get_topic_detail, name='topic_get'),
    path('create/', views.create_topic, name='topic_create'),
    path('<int:topic_id>/update/', views.update_topic, name='topic_update'),
    path('<int:topic_id>/delete/', views.delete_topic, name='topic_delete'),
]
# print("i'm quitting school and becoming a gas station attendant")