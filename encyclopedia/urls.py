from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("search",views.search,name="search"),
    path("edit/<title>", views.edit, name="edit"),
    path("random", views.random_page, name="random"),
]
