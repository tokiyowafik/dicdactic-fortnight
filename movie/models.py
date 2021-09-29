from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Movie(models.Model):
    RATE_G = 'G'
    RATE_PG = 'PG'
    RATE_PG13 = 'PG13'
    RATE_NC17 = 'NC17'
    RATE_CHOICES = [
        (RATE_G, 'G'),
        (RATE_PG, 'PG'),
        (RATE_PG13, 'PG-13'),
        (RATE_NC17, 'NC-17'),
    ]
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    daily_rate = models.FloatField()
    director = models.CharField(max_length=255)
    rate = models.CharField(max_length=4, choices=RATE_CHOICES, default=RATE_G)
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.title
