from django.db import models
from django.contrib.auth.models import User



# 用于存储电影类型。Used to store movie genres.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 用于存储电影的基本信息。# Used to store basic information of movies.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year_made = models.IntegerField()
    poster_url = models.URLField()
    genres = models.ManyToManyField(
        Genre, related_name="movies"
    )  # table Genre with table Movie:many to many

    def __str__(self):
        return self.title


# 用于存储用户对电影的评价 Used to store users' reviews of movies
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


# 每个用户有一个 Watch_list# Each user has one Watch_list.
class Watch_list(models.Model):
    # table User with table Watch_list:one to one
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1对1 one to one
    movies = models.ManyToManyField(Movie, related_name="watchlists")  # 多对多 many to many

    def __str__(self):
        return f"{self.user.username}'s WatchList"


# 每个用户有一个 My_movies   # Each user has one My_movies.
class My_movies(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)# 1对1 one to one
    movies = models.ManyToManyField(Movie, related_name="mymovies")   # 多对多 many to many

    def __str__(self):
        return f"{self.user.username}'s MyMovies"
