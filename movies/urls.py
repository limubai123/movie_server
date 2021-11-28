from django.urls import path

from movies.views import CreateGenreAPI, FevouriteGenreAPI

urlpatterns = [
    path("create_genre/", CreateGenreAPI.as_view()),
    path("fev_genre/", FevouriteGenreAPI.as_view()),
]
