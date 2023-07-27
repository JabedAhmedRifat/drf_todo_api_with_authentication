from django.urls import path

from .views import * 
from knox import views as knox_views

urlpatterns = [
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginApi.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('get_user/', UserAPI.as_view()),
]
