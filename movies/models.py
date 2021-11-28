from core.models import AbstractBaseModel
from django.contrib.auth.models import User
from django.db import models


class Genre(AbstractBaseModel):
    name = models.CharField(max_length=250, null=False)


class UserGenre(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)


class Movie(AbstractBaseModel):
    """
    Movie Model
    """

    name = models.CharField(max_length=250, null=False, db_index=True)
    genre = models.ManyToManyField(Genre)
    release_date = models.DateField(null=False)
    description = models.TextField(max_length=250, null=False, default=None)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-release_date"]


class Review(AbstractBaseModel):
    """
    Review Model
    """

    title = models.CharField(max_length=250, null=False)
    description = models.TextField(null=False, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE, null=False)


class Vote(AbstractBaseModel):
    """
    Vote Model
    """

    DOWN = "D"
    UP = "U"
    VOTING_CHOICES = [(DOWN, "Down"), (UP, "Up")]

    vote_nature = models.CharField(max_length=1, choices=VOTING_CHOICES, default=UP)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=False)
