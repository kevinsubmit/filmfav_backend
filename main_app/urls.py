from django.urls import path
from .views import Home, CreateUserView, LoginView, MovieView,  MovieView, MovieDetailView, WatchListView, AddToWatchListView,RemoveFromWatchListView

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('movies/', MovieView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),  
    path('watchlist/', WatchListView.as_view(), name='watchlist'),
    path('watchlist/add/<int:pk>/', AddToWatchListView.as_view(), name='add-to-watchlist'),
    path('watchlist/remove/<int:pk>/', RemoveFromWatchListView.as_view(), name='remove-from-watchlist'),

]
