"""Defines URL patterns for dataVis"""

from django.urls import path
from . import views

app_name = "dataVis"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    path("single/", views.single, name="single"),
    path("total/", views.total, name="total"),
]
