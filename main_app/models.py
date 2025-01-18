from django.db import models
from django.contrib.auth.models import User
# 用于存储用户的基本信息。# Used to store basic user information.
# no need django already do it for us

# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     password_hash = models.CharField(max_length=255)

#     def __str__(self):
#         return self.username


# 用于存储电影的基本信息。# Used to store basic information of movies.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year_made = models.IntegerField()
    poster_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 # 用于存储电影类型。Used to store movie genres.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# movie_genre 中间表模型（多对多关系）
# 通过中间表将电影与类型关联起来。
# movie_genre intermediate table model (many-to-many relationship)
# Associate movies with genres through the intermediate table.


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("movie", "genre")  # 联合唯一约束# Join unique constraint

    def __str__(self):
        return f"{self.movie.title} - {self.genre.name}"


# 用于存储用户对电影的评价 Used to store users' ratings of movies
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"


# 用于存储对电影评价的评论。Used to store comments about movie reviews.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.movie.title}"


# 每个用户有一个 watch_list。# Each user has one watch_list.
class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s WatchList"


# 表示用户 watch_list 下的多部电影。# indicates multiple movies under the user's watch_list.
class WatchListMovie(models.Model):
    watch_list = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "watch_list",
            "movie",
        )  # 联合唯一约束 # Join unique constraint

    def __str__(self):
        return f"{self.watch_list.user.username} added {self.movie.title} to WatchList"


# 每个用户有一个 my_movies。# Each user has one my_movies.
class MyMovies(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s MyMovies"


# my_movies_movie 中间表模型（多对多关系）
# 表示用户 my_movies 下的多部电影。
# my_movies_movie intermediate table model (many-to-many relationship)
# Represents multiple movies under the user my_movies.


class MyMoviesMovie(models.Model):
    my_movies = models.ForeignKey(MyMovies, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("my_movies", "movie")  # 联合唯一约束# Join unique constraint

    def __str__(self):
        return f"{self.my_movies.user.username} watched {self.movie.title}"
