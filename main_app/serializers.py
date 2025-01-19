from rest_framework import serializers

from django.contrib.auth.models import User # add this line to list of imports
from .models import Movie, Genre, WatchList, WatchListMovie, Review, Comment
from django.contrib.auth.models import User  # add this line to list of imports

from .models import Review, Comment

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
        #   email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source='genres',
        write_only=True,
        required=False
    )
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 
            'title', 
            'description', 
            'year_made', 
            'poster_url', 
            'genres', 
            'genre_ids',
            'average_rating', 
            'created_at'
        ]
    
    def get_average_rating(self, obj):
        reviews = Review.objects.filter(movie=obj)
        if reviews.exists():
            return sum(float(review.rating) for review in reviews) / reviews.count()
        return None

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'username', 'movie_title', 'movie', 'text', 'rating', 'created_at']
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'username', 'review', 'text', 'created_at']
        read_only_fields = ['user']

class WatchListMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    
    class Meta:
        model = WatchListMovie
        fields = ['id', 'movie', 'movie_id']
        read_only_fields = ['watch_list']

class WatchListSerializer(serializers.ModelSerializer):
    movies = WatchListMovieSerializer(source='watchlistmovie_set', many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = WatchList
        fields = ['id', 'user', 'movies', 'added_at']
        read_only_fields = ['user']
      
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "movie", "text", "rating", "created_at"]
        read_only_fields = ["user"]  # 将 user 字段标记为只读

    def create(self, validated_data):
        # 获取当前请求的用户
        user = self.context["request"].user  # 通过上下文获取当前用户
        validated_data["user"] = user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "review", "text", "created_at"]

