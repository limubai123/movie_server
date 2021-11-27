from django.urls import path

from movies.views import CreateGenreAPI

urlpatterns = [
    path("create_genre/", CreateGenreAPI.as_view()),
]
