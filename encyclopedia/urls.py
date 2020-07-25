from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entryTitle>", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/<title>", views.edit, name="edit"),
    path("randomEntry/", views.randomEntry, name="randomEntry")
]
