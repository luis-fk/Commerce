from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings

from . import models


def index(request):
    return render(request, "auctions/index.html", {
        "user": request.user,
        "listings": models.listings.objects.all().order_by('-id'),
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
        displayName = request.POST["displayName"]
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
            user = models.User.objects.create_user(username, email, password, displayName=displayName)
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
def newListing(request):
    if request.method == "POST":
        # Getting all info from request.
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image = request.POST["image"]
        categoryName = request.POST.get("category")

        # Error handling and some edge cases
        if not title:
            messages.error(request, "New listing must have a title!")
            return render(request, "auctions/newListing.html", {
                "category": models.category.objects.all()
            })
        if not categoryName:
            messages.error(request, "New listing must have a category!")
            return render(request, "auctions/newListing.html", {
                "category": models.category.objects.all()
            })
        elif not bid:
            bid = 0
        elif not image:
            image = "https://tinyurl.com/4wrmfwj2"
            
        # Create new listing
        currentUser = request.user
        category = models.category.objects.get(name=categoryName)
        currentUser.userListings.create(user=currentUser,
            title=title,
            description=description,
            bidValue=bid,  
            image=image,
            category=category,
        )
        
        return render(request, "auctions/index.html", {
            "user": currentUser,
            "listings": models.listings.objects.all().order_by('-id'),
        })

    else:
        print(request.user)
        return render(request, "auctions/newListing.html", {
            "category": models.category.objects.all()
        })


def listingPage(request, title, id):
    if request.method == "POST":
        currentUser = request.user
        listing = models.listings.objects.get(id=id)
        
        # Handles the posting of a new comment
        if "commentButton" in request.POST and request.user.is_authenticated:
            comment = request.POST["comment"]
            newComment = models.comment.objects.create(user=currentUser, text=comment)
            listing.comment.add(newComment)
            
            return render(request, "auctions/listingPage.html", {
                "user": request.user,
                "listing": listing,
            })
        
        # Handles adding a listing to watchlist
        elif "addWatchlist" in request.POST and request.user.is_authenticated:
            currentUser.userWatchlist.add(listing)
            
            return render(request, "auctions/watchlist.html", {
                "user": request.user,
            })
        
        # Handles removing an item from watchlist
        elif "removeFromWatchlist" in request.POST and request.user.is_authenticated:
            id = request.POST["id"]
            currentUser = request.user
            listing = models.listings.objects.get(id=id)
            currentUser.userWatchlist.remove(listing)
            
            return render(request, "auctions/watchlist.html", {
                "user": currentUser,
            })
        
        # Handles bidding on a listing
        elif "bidButton" in request.POST and request.user.is_authenticated:
            bid = int(request.POST["bidAmount"]) 
            
            if bid <= listing.bidValue:
                messages.error(request, "Bid must be higher than the current bid!")
                return render(request, "auctions/listingPage.html", {
                    "user": request.user,
                    "listing": listing,
                })

            # Creates a new bid
            models.bid.objects.create(user=currentUser, listing=listing)
            listing.bidValue = bid
            listing.save()
            
            return render(request, "auctions/listingPage.html", {
                "user": request.user,
                "listing": listing
            })
        
        # Handles closing of a listing
        elif "closeListing" in request.POST and request.user.is_authenticated:
            # This gets the last bidder for the current listing
            bidDetails = models.bid.objects.filter(listing=listing).order_by('-id').first()
            # Check if anyone bid on it
            if bidDetails:
                listing.winner = bidDetails.user
                listing.status = False
                listing.save()
            # If no bidder, there is no winner
            else:
                listing.winner = None
                listing.status = False
                listing.save()
            return render(request, "auctions/index.html", {
                "user": currentUser,
                "listings": models.listings.objects.all().order_by('-id')
            })
            
    else:
        return render(request, "auctions/listingPage.html", {
            "user": request.user,
            "listing": models.listings.objects.get(id=id)
        })
        

@login_required  
def watchlist(request): 
    if request.method == "POST":
        id = request.POST["id"]
        currentUser = request.user
        listing = models.listings.objects.get(id=id)
        # A user on his watchlist will only be able to remove a listing from it
        currentUser.userWatchlist.remove(listing)
        
        return render(request, "auctions/watchlist.html", {
            "user": currentUser,
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "user": request.user,
        })


@login_required
def myListings(request):
    return render(request, "auctions/myListings.html", {
        "user": request.user,
        "listings": models.listings.objects.all().order_by('-id')
    })
    
    
def closedListings(request):
    return render(request, "auctions/closedListings.html", {
        "user": request.user,
        "listings": models.listings.objects.all().order_by('-id'),
    })
    

@login_required
def categories(request):
    if request.method == "POST":
        categoryName = request.POST.get("category")
        category = models.category.objects.get(name=categoryName)
        listing = models.listings.objects.filter(category=category).order_by('-id')
            
        return render(request, "auctions/categories.html", {
            "user": request.user,
            "listings": listing,
            "category": models.category.objects.all()
        })
        
    else:
        return render(request, "auctions/categories.html", {
            "user": request.user,
            "listings": models.listings.objects.all().order_by('-id'),
            "category": models.category.objects.all()
        })
    
    
        
