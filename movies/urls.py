from django.urls import path

from movies.views import CreateGenreAPI, FevouriteGenreAPI, MovieAPI, RecomendedMovieAPI

urlpatterns = [
    path("create_genre/", CreateGenreAPI.as_view()),
    path("fev_genre/", FevouriteGenreAPI.as_view()),
    path("movie/", MovieAPI.as_view()),
    path("get_recomended_movie/", RecomendedMovieAPI.as_view()),
]
