from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('profile/update/', views.update_user_profile, name='update_user_profile'),
    path('profile/delete/', views.delete_user_profile, name='delete_user_profile')
]
# print("i'm quitting school and becoming a gas station attendant")