from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate

from movies.models import Genre, Movie, Review, Vote


class GenreTestCase(TestCase):
    """
    genre endpoints test cases
    """

    def setUp(self):
        Genre.objects.create(name="War")
        Genre.objects.create(name="Comedy")

    def test_fev_genre_endpoint_without_authentication(self):
        client = APIClient()
        response = client.post("/api/movie/fev_genre/", {"genre_id": 1}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_fev_genre_endpoint_with_authentication(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post("/api/movie/fev_genre/", {"genre_id": 1}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Record created")

    def test_fev_genre_endpoint_with_authentication_already_fevourite(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post("/api/movie/fev_genre/", {"genre_id": 1}, format="json")
        response = client.post("/api/movie/fev_genre/", {"genre_id": 1}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Genre is already a fevourite")

    def test_fev_genre_endpoint_with_authentication_genre_id_missing(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post("/api/movie/fev_genre/", {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "genre id is not given.")


class MovieTestCase(TestCase):
    """
    movie endpoints test cases
    """

    def setUp(self):
        Genre.objects.create(name="War")
        Genre.objects.create(name="Comedy")

    def test_movie_endpoint_without_authentication(self):
        client = APIClient()
        response = client.post(
            "/api/movie/movie/",
            {"name": "testMovie", "genre": [1, 2], "release_date": "2019-12-15", "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_movie_endpoint_with_authentication(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/movie/movie/",
            {"name": "testMovie", "genre": [1, 2], "release_date": "2019-12-15", "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_movie_endpoint_with_authentication_already_present(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/movie/movie/",
            {"name": "testMovie", "genre": [1, 2], "release_date": "2019-12-15", "description": "desc"},
            format="json",
        )
        response = client.post(
            "/api/movie/movie/",
            {"name": "testMovie", "genre": [1, 2], "release_date": "2019-12-15", "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_movie_endpoint_with_authentication_genre_not_exist(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/movie/movie/",
            {"name": "testMovie", "genre": [4], "release_date": "2019-12-15", "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_recomended_movie_endpoint_without_authentication(self):
        client = APIClient()
        response = client.get(
            "/api/movie/get_recomended_movie/",
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_get_recomended_movie_endpoint_with_authentication(self):
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            "/api/movie/get_recomended_movie/",
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_public_movies_endpoint(self):
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])
        client = APIClient()
        response = client.get(
            "/api/movie/public_movies/",
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_movie_detail_endpoint_without_authentication(self):
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])
        client = APIClient()
        response = client.get(
            "/api/movie/movie_detail/1/",
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_movie_detail_endpoint_with_authentication(self):
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])
        client = APIClient()
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client.force_authenticate(user=user)
        response = client.get(
            "/api/movie/movie_detail/1/",
            format="json",
        )
        self.assertEqual(response.status_code, 200)


class ReviewTestCase(TestCase):
    """
    review endpoints test cases
    """

    def setUp(self):
        Genre.objects.create(name="War")
        Genre.objects.create(name="Comedy")
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])

    def test_review_endpoint_without_authentication(self):
        client = APIClient()
        response = client.post(
            "/api/movie/review/",
            {"title": "reviewMovie", "movie": 1, "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_review_endpoint_with_authentication(self):
        client = APIClient()
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/movie/review/",
            {"title": "reviewMovie", "movie": 1, "description": "desc"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)


class VoteTestCase(TestCase):
    """
    vote endpoints test cases
    """

    def setUp(self):
        Genre.objects.create(name="War")
        Genre.objects.create(name="Comedy")

    def test_vote_endpoint_without_authentication(self):
        client = APIClient()
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])
        response = client.post(
            "/api/movie/vote/",
            {"vote_nature": "U", "movie": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_review_endpoint_with_authentication(self):
        client = APIClient()
        user = User.objects.create(username="test")
        user.set_password("12345")
        user.save()
        client.force_authenticate(user=user)
        movie = Movie.objects.create(name="bond", release_date="2018-9-1", description="desc")
        movie.genre.set([1, 2])
        response = client.post(
            "/api/movie/vote/",
            {"vote_nature": "U", "movie": 1},
            format="json",
        )
        movie.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(movie.upvote_count, 1)
        self.assertEqual(movie.downvote_count, 0)
        response = client.post(
            "/api/movie/vote/",
            {"vote_nature": "D", "movie": 1},
            format="json",
        )
        movie.refresh_from_db()
        self.assertEqual(movie.upvote_count, 0)
        self.assertEqual(movie.downvote_count, 1)
