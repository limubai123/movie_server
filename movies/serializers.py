from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movies.models import Genre, UserGenre


class CreateGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Genre.objects.all())])

    class Meta:
        model = Genre
        fields = ("name",)


class FevouriteGenreSerializer(serializers.Serializer):
    genre_name = serializers.SerializerMethodField()

    def get_genre_name(self, obj):
        return obj.genre.name
