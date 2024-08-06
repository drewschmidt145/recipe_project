from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    recipes_home,
    search,
    create_view,
    about,
)

app_name = "recipes"

urlpatterns = [
    path("home/", recipes_home, name="home"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<int:pk>/", RecipeDetailView.as_view(), name="detail"),
    path("search/", search, name="search"),
    path("create/", create_view, name="create"),
    path("about/", about, name="about"),
]
