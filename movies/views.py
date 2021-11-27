from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from movies.models import Genre, Movie, Review, Vote
from movies.serializers import CreateGenreSerializer


class CreateGenreAPI(generics.CreateAPIView):
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateGenreSerializer
