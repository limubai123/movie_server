from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movies.models import Genre


class CreateGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Genre.objects.all())])

    class Meta:
        model = Genre
        fields = ("name",)

    def create(self, validated_data):
        genre = Genre.objects.create(
            name=validated_data["name"],
        )

        return genre
