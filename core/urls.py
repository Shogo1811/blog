from django.urls import path

from core import views


app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("tag/<str:tag_name>/", views.entry_list_per_tag, name="entry_list_per_tag"),
    path("api/entry/search", views.api_search_entry, name="search_entry"),
    path("api/entry/", views.api_entry, name="api_entry"),
    path("api/entry/recent_list", views.api_recent_entry_list, name="api_recent_entry_list"),
]