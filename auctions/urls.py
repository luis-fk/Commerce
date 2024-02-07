from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing/", views.newListing, name="newListing"),
    path("<slug:title>/<int:id>/", views.listingPage, name="listingPage"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("my-listings/", views.myListings, name="myListings"),
    path("closed-listings/", views.closedListings, name="closedListings"),
    path("categories/", views.categories, name="categories")
]
