from django.db.models.aggregates import Count
from django.contrib import admin, messages
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'movies_count']
    search_fields = ['title']

    @admin.display(ordering='movies_count')
    def movies_count(self, genre):
        query_str = '?' + urlencode({
            'genre__id': str(genre.id)
        })
        url = reverse('admin:movie_movie_changelist') + query_str
        return format_html("<a href='{}'>{}</a>", url, genre.movies_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            movies_count=Count('movie')
        )


class InventoryMovie(admin.SimpleListFilter):
    title = 'rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('>9', 'Best rating')
        ]

    def queryset(self, request, queryset):
        if (self.value() == '>9'):
            return queryset.filter(daily_rate__gt=9.0)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    actions = ['rate_g']
    autocomplete_fields = ['genres']
    list_display = ['title', 'daily_rate_status',
                    'rate', 'director', 'genres_count']
    search_fields = ['title']
    list_filter = ['genres', InventoryMovie]
    list_editable = ['rate']
    list_per_page = 10
    ordering = ['title', 'daily_rate']

    @admin.display(ordering='genres_count')
    def genres_count(self, movie):
        query_str = '?' + urlencode({
            'movie__id': str(movie.id)
        })
        url = reverse("admin:movie_genre_changelist") + query_str

        return format_html("<a href='{}'>{}</a>", url, movie.genres_count)

    @admin.display(ordering='daily_rate')
    def daily_rate_status(self, movie):
        if movie.daily_rate > 9.0:
            return 'Popular'
        return 'Average'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            genres_count=Count('genres')
        )

    @admin.action(description='Set rating to G')
    def rate_g(self, request, queryset):
        updated_count = queryset.update(rate='G')
        self.message_user(
            request,
            f'{updated_count} movies was successfully updated.',
            messages.WARNING
        )
