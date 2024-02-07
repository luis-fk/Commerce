from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    displayName = models.CharField(max_length=64, null=True, blank=True)
    userListings = models.ManyToManyField("listings", blank=True, related_name="listings")
    userWatchlist = models.ManyToManyField("listings", related_name="watchlist")
    
    def __str__(self):
        return f"{self.username}"
    
    
class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey("listings", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Bid made by {self.user} on {self.listing}"
    
    
class listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userListing")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2000, null=True, blank=True)
    bidValue = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length= 2000, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="winner")
    status = models.BooleanField(default=True)
    category = models.ForeignKey("category", on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    comment = models.ManyToManyField("comment", blank=True, related_name="comment")
    
    def __str__(self):
        return f"{self.title}"
                 
    
class category(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComment")
    text = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Comment made by {self.user}"
    
