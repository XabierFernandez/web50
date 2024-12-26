from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.get_entry, name='get_entry'),
    path("random/", views.random_entry, name="random_entry"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>/edit/", views.edit_entry, name="edit_entry"),
    path("new_entry/", views.new_entry, name="new_entry"),
]
