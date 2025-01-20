from django.contrib import admin

from .models import AuctionListing, Bid, Category, Comment, User, Watchlist

class UserAdmin(admin.ModelAdmin):
    list_display = ("id" , "username", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id" , "category_name")

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "owner", "active", "date")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Watchlist._meta.get_fields()]

class BidAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bid._meta.get_fields()]

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
  
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)