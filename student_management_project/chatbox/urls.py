from .views import *
from django.urls import path
from  knox import views as knox_views
urlpatterns = [

    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('update-user/', update_user, name='updateuser'),
    path('delete-user/', delete_user, name = 'delete_user'),
    path('get-student-details/', get_user, name='get_user')
]