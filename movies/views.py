from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movies.models import Genre, Movie, Review, UserGenre, Vote
from movies.serializers import CreateGenreSerializer, FevouriteGenreSerializer


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
