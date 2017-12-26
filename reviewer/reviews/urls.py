from django.urls import path

from . import views

urlpatterns = [
    path("review", views.review, name="review"),
    path("tags", views.tags, name="tags"),
    path("stats", views.stats, name="stats")
]
