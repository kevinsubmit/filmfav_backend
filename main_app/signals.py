# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Watch_list, My_movies

@receiver(post_save, sender=User)
def create_user_watchlist_and_mymovies(sender, instance, created, **kwargs):
    """
    当新用户创建时，自动创建一个空的 Watch_list 和 My_movies
    Automatically create an empty Watch_list and My_movies when a new user is created.
    """
    if created:
        # 为新用户创建一个空的 Watch_list 和 My_movies
        Watch_list.objects.create(user=instance)
        My_movies.objects.create(user=instance)
