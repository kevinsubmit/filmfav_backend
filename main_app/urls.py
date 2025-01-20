from django.urls import path

from .views import Home, CreateUserView, LoginView,ReviewListCreateAPIView,ReviewDetailAPIView,CommentListCreateAPIView,CommentDetailAPIView,MovieView,  MovieView, MovieDetailView, WatchListView, AddToWatchListView, RemoveFromWatchListView,  MyMoviesView, AddToMyMoviesView, RemoveFromMyMoviesView


urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'), 
    path('api/reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),  
    path('api/reviews/<int:review_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'), 
    path('api/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'), 
    path('movies/', MovieView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),  
    path('watchlist/', WatchListView.as_view(), name='watchlist'),
    path('watchlist/add/<int:pk>/', AddToWatchListView.as_view(), name='add-to-watchlist'),
    path('watchlist/remove/<int:pk>/', RemoveFromWatchListView.as_view(), name='remove-from-watchlist'),
    path('mymovies/', MyMoviesView.as_view(), name='mymovies'),
    path('mymovies/add/<int:pk>/', AddToMyMoviesView.as_view(), name='add-to-mymovies'),
    path('mymovies/remove/<int:pk>/', RemoveFromMyMoviesView.as_view(), name='remove-from-mymovies'),
]


