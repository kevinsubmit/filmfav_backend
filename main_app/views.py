

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, filters # modify these imports to match
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend



from .serializers import (
    UserSerializer,
    MovieSerializer,
    GenreSerializer,
    WatchListSerializer,
    WatchListMovieSerializer,
    ReviewSerializer,
)

from .models import Movie, Genre, WatchList, WatchListMovie, Review, Comment

# Create your views here.
class Home(APIView):
    def get(self,request):
        message = {'mes':'welcome'}
        return Response(message)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  
    refresh = RefreshToken.for_user(request.user)  
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })


class MovieView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            movie = self.get_object(pk)
            if movie is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        else:
            queryset = Movie.objects.all()
            
            filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
            for backend in filter_backends:
                queryset = backend().filter_queryset(request, queryset, self)
            
            serializer = MovieSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, pk=None):
        if pk:
            return Response(
                {"detail": "POST method not allowed with movie ID"}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response(
                {"detail": "Movie ID required for update"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        movie = self.get_object(pk)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response(
                {"detail": "Movie ID required for deletion"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        movie = self.get_object(pk)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def filter_queryset(self, queryset):
        return queryset

    filterset_fields = ['year_made', 'genres__name']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'year_made', 'created_at']

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MovieReviewsView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            movie_id=self.kwargs['pk']
        )

class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WatchListView(generics.ListCreateAPIView):
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if WatchList.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("User already has a watchlist")
        serializer.save(user=self.request.user)

class WatchListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

class AddToWatchListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            watchlist = WatchList.objects.get(user=request.user)
            serializer = WatchListMovieSerializer(data=request.data)
            
            if serializer.is_valid():
                try:
                    serializer.save(watch_list=watchlist)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response(
                        {"detail": "Movie already in watchlist"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response(
                {"detail": "Watchlist not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class RemoveFromWatchListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            watchlist = WatchList.objects.get(user=request.user)
            try:
                movie_id = request.data.get('movie_id')
                watchlist_movie = WatchListMovie.objects.get(
                    watch_list=watchlist,
                    movie_id=movie_id
                )
                watchlist_movie.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except WatchListMovie.DoesNotExist:
                return Response(
                    {"detail": "Movie not found in watchlist"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except WatchList.DoesNotExist:
            return Response(
                {"detail": "Watchlist not found"},
                status=status.HTTP_404_NOT_FOUND
            )