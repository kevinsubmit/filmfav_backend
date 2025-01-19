from django.urls import path
from .views import Home,CreateUserView,LoginView,ReviewListCreateAPIView,ReviewDetailAPIView,CommentListCreateAPIView,CommentDetailAPIView

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'), 
    path('api/reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),  
    path('api/reviews/<int:review_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'), 
    path('api/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'), 
]