from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class createListingModel(models.Model):         
    categoryChoices = (
        ('Fashion', 'Fashion'),
        ('Book', 'Book'),
        ('Electronics', 'Electronics'),
        ('Household', 'Household'),
        ('Art', 'Art'),
     )
    #Django adds autoincrement id by default
    title = models.CharField(max_length=40)
    startBid = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    description = models.CharField(max_length=400)
    category = models.CharField(max_length=100, choices=categoryChoices)
    imageUpload = models.ImageField()
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    winner = models.ForeignKey(User, related_name="winner", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class watchlistModel(models.Model):
    current_user = models.ForeignKey(User, related_name='watch', on_delete=models.CASCADE) 
    watchlist_product = models.ForeignKey(createListingModel, related_name='list', on_delete= models.CASCADE)  
                

class bidModel(models.Model):
    user = models.ForeignKey(User, related_name='userBids', on_delete=models.CASCADE) 
    product = models.ForeignKey(createListingModel, on_delete= models.CASCADE)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=3, default=0)


class commentModel(models.Model):
    content = models.TextField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(createListingModel, related_name='comments', on_delete= models.CASCADE)