from django.urls import path
from .views import (
    Home,
    CreateUserView,
    LoginView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView,
    MovieList,
    MovieCreate,
    MovieDetail,
    MovieUpdate,
    MovieDelete,
    WatchListDetail,
    AddMovieToWatchList,
    RemoveMovieFromWatchList,
    MyMoviesDetail,
    AddMovieToMyMovies,
    RemoveMovieFromMyMovies,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('users/register/', CreateUserView.as_view(), name="register"),
    path("users/login/", LoginView.as_view(), name="login"),
    path("reviews/", ReviewListCreateAPIView.as_view(), name="review-list-create"),
    path("reviews/movie/<int:movie_id>/", ReviewListCreateAPIView.as_view(), name="review-list-by-movie"),  # 获取电影评论
    path("reviews/<int:review_id>/", ReviewDetailAPIView.as_view(), name="review-detail"),  # 获取单个评论
    path("reviews/<int:review_id>/comments/", CommentListCreateAPIView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentDetailAPIView.as_view(), name="comment-detail"),
    path("movies/", MovieList.as_view(), name="movie-list"),
    path("movies/create/", MovieCreate.as_view(), name="movie-create"),
    path("movies/<int:pk>/", MovieDetail.as_view(), name="movie-detail"),
    path("movies/<int:pk>/update/", MovieUpdate.as_view(), name="movie-update"),
    path("movies/<int:pk>/delete/", MovieDelete.as_view(), name="movie-delete"),
    path("watchlist/", WatchListDetail.as_view(), name="watchlist-detail"),
    path("watchlist/add/", AddMovieToWatchList.as_view(), name="add-movie-to-watchlist"),
    path("watchlist/remove/", RemoveMovieFromWatchList.as_view(), name="remove-movie-from-watchlist"),
    path("mymovies/", MyMoviesDetail.as_view(), name="watchlist-detail"),
    path("mymovies/add/", AddMovieToMyMovies.as_view(), name="add-movie-to-watchlist"),
    path("mymovies/remove/", RemoveMovieFromMyMovies.as_view(), name="remove-movie-from-watchlist"),
]
