# myapp/management/commands/generate_fake_movies.py

from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Movie, Genre
import random

class Command(BaseCommand):
    help = 'Generate fake movie data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create some genres first if they don't exist
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Thriller']
        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)

        # Generate 200 fake Movie entries
        for _ in range(200):
            title = fake.sentence(nb_words=4)
            description = fake.text(max_nb_chars=200)
            year_made = fake.year()
            poster_url = fake.image_url()
            
            # Create the Movie instance
            movie = Movie.objects.create(
                title=title,
                description=description,
                year_made=year_made,
                poster_url=poster_url
            )

            # Get the list of genres and assign random genres to the movie (using ManyToManyField)
            genre_list = list(Genre.objects.all())  # Convert QuerySet to list
            movie.genres.set(random.sample(genre_list, random.randint(1, 3)))  # Assign 1 to 3 random genres

        self.stdout.write(self.style.SUCCESS('Successfully generated 200 fake movies'))
