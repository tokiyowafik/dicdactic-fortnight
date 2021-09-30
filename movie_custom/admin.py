from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from movie.admin import MovieAdmin
from movie.models import Movie
from tags.models import TaggedItem


class TaggedItemInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 1
    model = TaggedItem


class CustomMovieAdmin(MovieAdmin):
    inlines = [TaggedItemInline]


admin.site.unregister(Movie)
admin.site.register(Movie, CustomMovieAdmin)
