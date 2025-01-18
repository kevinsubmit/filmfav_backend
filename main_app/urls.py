from django.urls import path
from .views import Home,CreateUserView,LoginView

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
]
