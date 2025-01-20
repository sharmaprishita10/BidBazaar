from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from django import forms
from django.db.models import Max, Count

#Required to check whether the listing is in the list of dictionaries (Group by and aggregate)
class counter():
    count = 0
    def increment(self):
        self.count = self.count + 1
        return ""
    def back(self):
        self.count = 0
        return ""

#For Select input field
categories = Category.objects.all()
CATEGORY = [(category.id, category.category_name) for category in categories]

class NewListingForm(forms.Form):
    title = forms.CharField(label="", max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="" ,max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    starting_bid = forms.DecimalField(label="" ,max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control'}))
    image = forms.URLField(label="" , required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ChoiceField(label="" ,choices= CATEGORY, widget=forms.Select(attrs={'class':'form-control'}))

class BidForm(forms.Form):
    bid = forms.DecimalField(label="" ,max_digits=6, decimal_places=2)

def index(request):
    #Group by for max bid
    bid_list = Bid.objects.values('listing').annotate(max_bid=Max('bid'))       #list of dicts

    #Group by for watchers count
    watchers = Watchlist.objects.values('listing').annotate(user_count=Count('user'))

    listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "bid_list" : bid_list,
        "no" : counter(),
        "watchers" : watchers
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):                #For creating a new listing
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            user = request.user
            new = AuctionListing(
                title = title,
                description = description,
                starting_bid = starting_bid,
                image = image,
                category = Category.objects.get(pk=category),
                owner =user
            )
            new.save()
            messages.success(request, "New Auction Listing created successfully.")
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html" , {
        "form" : NewListingForm()
    })

def listing(request, listing_id):           #For Listing-specific page
    #Group by for max bid
    bid_list = Bid.objects.values('listing').annotate(max_bid=Max('bid'))       #list of dicts

    #Group by for no of bids
    bids = Bid.objects.values('listing').annotate(bid_count=Count('user'))

    #Group by for watchers count
    watchers = Watchlist.objects.values('listing').annotate(user_count=Count('user'))

    item = AuctionListing.objects.get(pk=listing_id)

    for dict in bid_list:                       #For finding the winner
        if dict["listing"] == listing_id:       #In case of any bids 
            bid = Bid.objects.get(bid = dict["max_bid"], listing=listing_id)
            if bid.winner:                      #If the listing is closed and the highest bid won
                winner = bid.user               #Declare the bid user as the winner
            else:
                winner = None           
        else:                                   #In case of 0 bids on the listing
            winner = None

    #For watchlist button title
    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist.filter(listing = listing_id).first()
        if in_watchlist:
            watchlist_title = "Remove from Watchlist"
        else:
            watchlist_title = "Add to Watchlist"
    else:
        watchlist_title = "Watch"

    count = 0      #counter for the for loop for the tag line below place bid
    for dict in bid_list:
        if dict["listing"] == listing_id:           #If there are bids placed already
            tag_line = f"Place a bid greater than US${round(dict['max_bid'], 2)}" 
        else:
            count += 1
    if count == len(bid_list):          #If no bids are placed yet
        tag_line = f"Place a bid greater than or equal to US${item.starting_bid}"

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        else:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.cleaned_data["bid"]
                #check whether any bid is placed already or not
                no = 0      #counter for the for loop
                for dict in bid_list:
                    if dict["listing"] == listing_id:
                        if bid > dict["max_bid"]:
                            new_bid = Bid(user = request.user, bid = bid, listing = item)
                            new_bid.save()
                            messages.success(request , "Your bid is placed successfully!")
                            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                        else:
                            messages.error(request , "Your bid is less than the highest bid. Try Again!")
                            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
                    else:
                        no += 1
                
                if no == len(bid_list):        #If there are no bids on this listing yet
                    if bid >= item.starting_bid:
                        new_bid = Bid(user = request.user, bid = bid, listing = item)
                        new_bid.save()
                        messages.success(request , "Your bid is placed successfully!")
                        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                        
                    else:
                        messages.error(request , "Your bid is less than the starting bid. Try Again!")
                        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    return render(request, "auctions/listing.html", {
        "listing" : item,
        "winner" : winner,
        "bids" : bids,
        "watchers" : watchers,
        "bid_list" : bid_list,
        "bid_form" :BidForm(),
        "tag_line" : tag_line,
        "watchlist_title" : watchlist_title,
        "comments" : item.comments.all()
    })

@login_required
def update_watch(request, listing_id):      #For updating the user's watchlist
    if request.method == "POST":
        in_watchlist = request.user.watchlist.filter(listing = listing_id).first()
        if in_watchlist:
            in_watchlist.delete()
            messages.success(request, "Removed from Watchlist successfully!")
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            listing = AuctionListing.objects.get(pk=listing_id)
            add_to_watchlist = Watchlist(user = request.user, listing = listing)
            add_to_watchlist.save()
            messages.success(request, "Added to Watchlist successfully!")
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def comment(request, listing_id):           #For posting a comment
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        comment = request.POST["comment"]
        new_comment = Comment(user = request.user, listing = listing, comment = comment)
        new_comment.save()
        messages.success(request , "Comment posted successfully!")
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def end_auction(request, listing_id):           #For ending the auction by the owner
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        listing.active = False                  #End the auction
        listing.save()

        #Group by for max bid
        bid_list = Bid.objects.values('listing').annotate(max_bid=Max('bid'))       #list of dicts
        for dict in bid_list:
            if dict["listing"] == listing_id:
                bid = Bid.objects.get(bid = dict["max_bid"], listing=listing_id)
                bid.winner = True               #Declare the bid as winning bid
                bid.save()
                messages.success(request, f"Auction ended!")
                return HttpResponseRedirect(reverse("listing" , args=[listing_id]))

@login_required
def watchlist(request):         #For displaying user's watchlist
    return render(request, "auctions/watchlist.html", {
        "watchlist" : request.user.watchlist.all()
    })

def listing_categories(request):        #For displaying all the categories
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all()
    })

def category(request, category_id):        #For displaying all the active listings in the specific category
    #Group by for max bid
    bid_list = Bid.objects.values('listing').annotate(max_bid=Max('bid'))       #list of dicts

    #Group by for watchers count
    watchers = Watchlist.objects.values('listing').annotate(user_count=Count('user'))

    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "active_listings" : category.category_auctions.filter(active=True),
        "bid_list" : bid_list,
        "no" : counter(),
        "watchers" : watchers,
        "category" : Category.objects.get(pk=category_id)
    })