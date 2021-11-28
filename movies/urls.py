from django.urls import path, re_path

from movies.views import (
    CreateGenreAPI,
    FevouriteGenreAPI,
    MovieAPI,
    MovieDetailAPI,
    RecomendedMovieAPI,
    ReviewAPI,
    VoteAPI,
)

urlpatterns = [
    path("create_genre/", CreateGenreAPI.as_view()),
    path("fev_genre/", FevouriteGenreAPI.as_view()),
    path("movie/", MovieAPI.as_view()),
    path("get_recomended_movie/", RecomendedMovieAPI.as_view()),
    path("review/", ReviewAPI.as_view()),
    path("vote/", VoteAPI.as_view()),
    re_path(r"^movie_detail/(?P<pk>\d+)/$", MovieDetailAPI.as_view()),
]
