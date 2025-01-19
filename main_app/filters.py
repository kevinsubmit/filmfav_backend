import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    
    genres = django_filters.CharFilter(field_name='genres__name', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title', 'year_made', 'genres']
