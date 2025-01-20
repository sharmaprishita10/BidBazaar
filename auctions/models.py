from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"Category - {self.category_name}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="category_auctions" )
    owner = models.ForeignKey(User, on_delete=models.CASCADE , related_name="creations")
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category}) - Active: {self.active}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchers")

    def __str__(self):
        return f"{self.listing} added to {self.user}'s Watchlist"
        
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bids")
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="placed_bids")
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} placed bid at US${self.bid} on {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="my_comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    comment_date = models.DateField(auto_now=True)
