from django.urls import path

from . import views


urlpatterns = [
    path("songbook/", views.songbook, name="songbook"),
    path("lyrics/", views.songlyrics, name="songlyrics"),
]
