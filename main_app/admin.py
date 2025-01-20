from django.contrib import admin
from .models import Movie, Genre, Review, Comment, Watch_list, My_movies

# Register your models here.
admin.site.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  list_display = ('title', 'year_made', 'created_at')
  list_filter = ('genres',)
  search_fields = ('title',)
  
admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
  list_display = ('name',)
  search_fields = ('name',)