from django.db.models import Subquery
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movies.models import Genre, Movie, Review, UserGenre, Vote
from movies.serializers import (
    CreateGenreSerializer,
    FevouriteGenreSerializer,
    MovieDetailSerializer,
    MovieSerializer,
    ReviewSerializer,
    VoteSerializer,
)


class CreateGenreAPI(generics.CreateAPIView):
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateGenreSerializer


class FevouriteGenreAPI(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FevouriteGenreSerializer

    def get(self, request, format=None):
        geners = UserGenre.objects.filter(user=request.user)
        serializer = self.serializer_class(geners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        genre_id = request.data.get("genre_id", None)
        if not genre_id:
            return Response({"message": "genre id is not given."}, status=status.HTTP_400_BAD_REQUEST)
        genre = Genre.objects.filter(id=genre_id).first()
        if genre:
            user_genre = UserGenre.objects.filter(user=request.user, genre=genre).first()
            if user_genre:
                return Response(
                    {"message": "Genre is already a fevourite"}, status=status.HTTP_400_BAD_REQUEST
                )
            UserGenre.objects.create(user=request.user, genre=genre)
            return Response({"message": "Record created"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)


class MovieAPI(generics.CreateAPIView):
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieSerializer


class RecomendedMovieAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        user_genres = UserGenre.objects.filter(user=self.request.user)
        return Movie.objects.filter(genre__in=user_genres.values("genre__id")).distinct()


class ReviewAPI(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get(self, request, format=None):
        reviews = Review.objects.filter(user=request.user)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serilaizer = self.serializer_class(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save(user=request.user)
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteAPI(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer

    def post(self, request, format=None):
        serilaizer = self.serializer_class(data=request.data, context={"request": request})
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPI(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    permission_classes = (IsAuthenticated,)
