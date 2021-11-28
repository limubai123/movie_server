from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movies.models import Genre, Movie, Review, UserGenre, Vote


class CreateGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Genre.objects.all())])

    class Meta:
        model = Genre
        fields = ("name",)


class FevouriteGenreSerializer(serializers.Serializer):
    genre_name = serializers.SerializerMethodField()

    def get_genre_name(self, obj):
        return obj.genre.name


class MovieSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Movie.objects.all())])

    class Meta:
        model = Movie
        fields = ("name", "genre", "release_date", "description")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "description", "movie")


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "description", "user__username")


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("vote_nature", "movie")

    def create(self, validated_data):
        vote = Vote.objects.filter(
            movie=validated_data.get("movie"),
            user=self.context.get("request").user,
        ).first()

        if not vote:
            vote = Vote(movie=validated_data.get("movie"), user=self.context.get("request").user)

        vote.vote_nature = validated_data.get("vote_nature")
        vote.save()
        return vote


class MovieDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "name",
            "genre",
            "release_date",
            "description",
            "upvote_count",
            "downvote_count",
            "reviews",
        )

    def get_reviews(self, obj):
        return ReviewDetailSerializer(Review.objects.filter(movie=obj), many=True)
