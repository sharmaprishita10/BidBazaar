from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/update_watch", views.update_watch,  name="update_watch"),
    path("<int:listing_id>/comment" , views.comment, name="comment"),
    path("<int:listing_id>/end", views.end_auction, name="end_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.listing_categories, name="categories"),
    path("<int:category_id>/category", views.category, name="category")
]
