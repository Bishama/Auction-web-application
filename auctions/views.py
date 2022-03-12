from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, createListingModel, watchlistModel, bidModel, commentModel
from .forms import createListingForm, commentForm

def index(request):
    #{Model -> View -> Index.html}
    data = createListingModel.objects.all()
    empty = False
    if len(data) == 0:
       empty=True
    return render(request, "auctions/index.html", {
        "data": data,
        "empty": empty
    })


def watchlist(request):                
    user = User.objects.get(username=request.user)
    # Get all products in watchlist model for the specific user
    watchlist_items = user.watch.all() 
    present = False
    if watchlist_items:
         present = True
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items,                    #gIVE ALL thewatchlistModel objects
        "present" : present
    })
     
    
          
def categories(request):
    pass


def bid(request, id):
    #1.Get current user
    user = User.objects.get(username=request.user)
    #2.Get the product
    data = createListingModel.objects.get(id=id)
#3. Get the price submitted via form
    input_bid_price = float(request.POST["bidPrice"]) 
    #Print 1 2 3
    print(user, data.startBid, input_bid_price)
    
#5 Get the highest bid so far. If o bid has been placed set max-bid to the starting price(by seller)
    if bidModel.objects.filter(product=data):
        max_bid = bidModel.objects.filter(product=data).order_by('-highest_bid').first().highest_bid
        #Print 5
        print(max_bid)
    else:
        max_bid = data.startBid

#4.Make sure bid placed is higher than initialprice and currentbid and Save user, product, bidPrice in model (bid)
    if input_bid_price > max_bid:
        bidInstance = bidModel.objects.create(user = user,product = data, highest_bid = input_bid_price)                     #Instance of bid model
        bidInstance.save()
    else:
        return HttpResponse('Bid should be higher than the existing bid')

    return render(request, "auctions/index.html")




def listing(request, id):
    data = createListingModel.objects.get(id=id)            
    user = User.objects.get(username=request.user)
    watchlist = watchlistModel()
    form = commentForm()
    #5. Hishest bid
    if bidModel.objects.filter(product=data):
        max_bid = bidModel.objects.filter(product=data).order_by('-highest_bid').first().highest_bid
    else:
        max_bid = data.startBid
    #6 Winner
    if bidModel.objects.filter(product=data):
        winner = bidModel.objects.get(highest_bid = max_bid).user
    else:
        winner = request.user
    print(winner)
    #7 Show comments in html 
    print( data.comments.all())

    if request.method == 'POST':                  
        #If close auction button clicked and the currnet user is the owner, inactivate the listing
        if "closeListing" in request.POST:
            data.active = False
            data.save()
            print(data.active)

        #If comment button clicked
        if "addComment" in request.POST:
            commentInstance = commentModel(author=user, product=data)
            commentInstance.content = request.POST["content"]
            commentInstance.save()

        #If watchlist button clicked
        if "watchlist" in request.POST and not watchlistModel.objects.filter(watchlist_product= data):
            watchlist.watchlist_product = data
            watchlist.current_user = user
            watchlist.save()
        #When watchlist button clicked on listing html, remove the id from db
        else:
            user.watch.filter(watchlist_product=data).delete()


    #GET request return simple html
    return render(request, "auctions/listing.html", {
        "user": request.user,
        "data": data,
        "highest_bid": max_bid,
        "winner": winner, 
        "form" : form
    })

                             


def createListing(request):
    #Form submited
    if request.method == 'POST':
        #Get the form data submitted throught createListing.html and store in database
        form = createListingForm(request.POST , request.FILES)
        #Before storing the data access cleaned data (in dictionary form) otherwise it will be whole html 
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller= request.user        #Save the owner who created the listing
            listing.save()
        return HttpResponseRedirect(reverse('index'))
    #else render html
    else:
        form = createListingForm()
        return render(request, "auctions/createlisting.html", {
        "form": form 
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