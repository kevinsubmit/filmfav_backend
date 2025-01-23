from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from rest_framework import (
    generics,
    status,
    permissions,
    filters,
)

# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import (
    UserSerializer,
    GenreSerializer,
    MovieSerializer,
    CommentSerializer,
    ReviewSerializer,
    Watch_listSerializer,
    My_moviesSerializer,
)

from .models import Movie, Genre, Review, Comment, Watch_list, My_movies


# Create your views here.
class Home(APIView):
    def get(self, request):
        message = {"mes": "welcome"}


from rest_framework import (
    generics,
    status,
    permissions,
)  # modify these imports to match
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Review, Comment
from django.shortcuts import get_object_or_404


# Create your views here.
class Home(APIView):
    def get(self, request):
        message = {"mes": "weclome"}
        return Response(message)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Check if username already exists
        username = request.data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": ["A user with that username already exists."]})

        # Proceed with the usual create process if the username is unique
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        
        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": response.data,
            },
            status=status.HTTP_201_CREATED  # Status for successful creation
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                }
            )
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# User Verification
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(request.user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


# 拿到所有电影 movies (GET)
class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)



class MoviePagination(PageNumberPagination):
    page_size = 20  
    page_size_query_param = 'page_size'
    max_page_size = 100  

class MovieListView(APIView):
    def get(self, request):
    
        movies = Movie.objects.all()
        paginator = MoviePagination()
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# 增加电影 movies (POST)
class MovieCreate(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        movie_data = request.data.get("movies", [])
        serializer = MovieSerializer(data=movie_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 拿到一部具体电影 get one movie‘s detail (GET)
class MovieDetail(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)


# 更新一部电影  update one movie (PUT)
class MovieUpdate(APIView):
    permission_classes = [permissions.IsAdminUser]
    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 删除一部电影 delete one movie (DELETE)
class MovieDelete(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(
            {"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


# 获取当前用户的 WatchList /get the current user's WatchList
class WatchListDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            watch_list = Watch_list.objects.get(user=request.user)
        except Watch_list.DoesNotExist:
            return Response(
                {"detail": "Watch list not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = Watch_listSerializer(watch_list)
        return Response(serializer.data)


# 将电影添加到用户的 WatchList / add the movie to the user's WatchList
class AddMovieToWatchList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_ids = request.data.get("movie_ids", [])
        if not movie_ids:
            return Response(
                {"detail": "No movie IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movies = Movie.objects.filter(id__in=movie_ids)

        if not movies:
            return Response(
                {"detail": "One or more movies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            watch_list = Watch_list.objects.get(user=request.user)
        except Watch_list.DoesNotExist:
            return Response(
                {"detail": "Watch list not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        watch_list.movies.add(*movies)
        return Response(
            {"detail": f"{len(movies)} movie(s) added to your watchlist."},
            status=status.HTTP_200_OK,
        )


# 从用户的 WatchList 中删除电影/ remove the movie from the user's WatchList
class RemoveMovieFromWatchList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_ids = request.data.get("movie_ids", [])

        if not movie_ids:
            return Response(
                {"detail": "No movie IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movies = Movie.objects.filter(id__in=movie_ids)

        if not movies:
            return Response(
                {"detail": "One or more movies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            watch_list = Watch_list.objects.get(user=request.user)
        except Watch_list.DoesNotExist:
            return Response(
                {"detail": "Watch list not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        watch_list.movies.remove(*movies)

        return Response(
            {"detail": f"{len(movies)} movie(s) removed from your watchlist."},
            status=status.HTTP_200_OK,
        )


# 获取当前用户的 MyMovies /get the current user's MyMovies
class MyMoviesDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            my_movies = My_movies.objects.get(user=request.user)
        except My_movies.DoesNotExist:
            return Response(
                {"detail": "My movies list not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = My_moviesSerializer(my_movies)
        return Response(serializer.data)


# 将电影添加到用户的 MyMovies /add the movie to the user's MyMovies
class AddMovieToMyMovies(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_ids = request.data.get("movie_ids", [])
        
        if not movie_ids:
            return Response(
                {"detail": "No movie IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        movies = Movie.objects.filter(id__in=movie_ids)
        if not movies.exists():
            return Response(
                {"detail": "One or more movies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            my_movies = My_movies.objects.get(user=request.user)
        except My_movies.DoesNotExist:
            return Response(
                {"detail": "MyMovies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        my_movies.movies.add(*movies)

        return Response(
            {"detail": f"{len(movies)} movie(s) added to your MyMovies."},
            status=status.HTTP_200_OK,
        )


# 从用户的 MyMovies 中删除电影  remove the movie from the user's MyMovies
class RemoveMovieFromMyMovies(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_ids = request.data.get("movie_ids", [])
        
        if not movie_ids:
            return Response(
                {"detail": "No movie IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        movies = Movie.objects.filter(id__in=movie_ids)
        if not movies.exists():
            return Response(
                {"detail": "One or more movies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            my_movies = My_movies.objects.get(user=request.user)
        except My_movies.DoesNotExist:
            return Response(
                {"detail": "MyMovies not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        my_movies.movies.remove(*movies)

        return Response(
            {"detail": f"{len(movies)} movie(s) removed from your MyMovies."},
            status=status.HTTP_200_OK,
        )

# Review API
class ReviewListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Get all reviews for a specific movie
    def get(self, request, movie_id=None):
        if movie_id:
            # Filter reviews by movie_id
            reviews = Review.objects.filter(movie__id=movie_id)
        else:
            # Get all reviews if no movie_id is provided
            reviews = Review.objects.all()
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    # create the review
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  # 不需要传递任何参数,自动将 user 添加到 validated_data 中并保存
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# single Review （get、update、delete）
class ReviewDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        if review.user != request.user:
            return Response(
                {
                    "detail":"you do not have permission to edit this review."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        if review.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this review."},
                status=status.HTTP_403_FORBIDDEN
            )
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Comment API (get、update、delete）
class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 获取某个评论下的所有评论  get one specfiec review's all comments
    def get(self, request, review_id):
        comments = Comment.objects.filter(review__id=review_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 创建某个评论下的单条评论 create one specfiec review's one comment
    def post(self, request, review_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user, review_id=review_id
            )  # 将评论与评论和当前用户关联  connect review with presnet user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 单个 Comment 视图（获取、删除） get the signle Comment's detail
class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
