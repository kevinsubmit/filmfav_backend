from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Genre, Review, Comment, Watch_list, My_movies


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password is write-only

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],  # password is hashed
        )
        return user


# Genre Serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    # genres 是 ManyToMany 关系，所以我们使用 GenreSerializer 序列化相关数据
    # genres is a ManyToMany relationship, so we use GenreSerializer to serialize related data
    genres = GenreSerializer(many=True, read_only=True)

    # genre_ids 是接收前端传过来的 Genre ID，用于多对多关系的更新
    # genre_ids is used to receive Genre IDs from the frontend for updating the many-to-many relationship
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source="genres",
        write_only=True,
        required=False,
    )

    # average_rating 是一个计算字段，用来返回电影的平均评分
    # average_rating is a computed field to return the movie's average rating
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "year_made",
            "poster_url",
            "genres",
            "genre_ids",
            "average_rating",
        ]

    def get_average_rating(self, obj):
        # 计算电影的平均评分
        # Calculate the movie's average rating
        reviews = Review.objects.filter(movie=obj)
        if reviews.exists():
            return sum(float(review.rating) for review in reviews) / reviews.count()
        return None


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)  # 显示用户名 / Display the username
    movie_title = serializers.CharField(source="movie.title", read_only=True)  # 显示电影标题 / Display the movie title

    class Meta:
        model = Review
        fields = [
            "id",
            "username",  # 额外的字段：用户名 / Additional field: Username
            "movie_title",  # 额外的字段：电影标题 / Additional field: Movie title
            "movie",  # 外键字段 movie / Foreign key field movie
            "text",  # 评论内容 / Review content
            "rating",  # 评分 / Rating
            "created_at",  # 创建时间 / Creation timestamp
        ]
        read_only_fields = ["user"]  # user 字段通过 create 方法自动处理 / The user field is handled automatically in the create method

    def create(self, validated_data):
        # 自动绑定当前请求的用户到 review 的 user 字段
        # Automatically bind the current user from the request to the 'user' field of the review
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "username", "review", "text", "created_at"]
        read_only_fields = ["user"]


# Watch_list Serializer
class Watch_listSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(
        many=True, read_only=True
    )  # 直接通过 MovieSerializer 显示电影 / Directly display movies using MovieSerializer
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Watch_list
        fields = ["id", "user", "movies"]
        read_only_fields = ["user"]


# My_movies Serializer
class My_moviesSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(
        many=True, read_only=True
    )  # 直接通过 MovieSerializer 显示电影 / Directly display movies using MovieSerializer
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = My_movies
        fields = ["id", "user", "movies"]
        read_only_fields = ["user"]
