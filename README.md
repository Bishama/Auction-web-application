# Auction-web-application

## Functionality

### Models: 
Application have four models: one for auction listings, one for bids, one for watchlist and one for comments made on auction listings. <br>

### Create Listing: 
Users are able to visit a page to create a new listing. Users can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also upload the image of the listing and choose a category (e.g. Fashion, Toys, Electronics, Home, etc.) <br>

### Active Listings Page:
Users are able to see all the current active listings on the default page <br>

### Listing Page:
<li>Clicking on a listing takes the users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing 
<li>If the user is signed in, the users are able to add the item to their “Watchlist.” If the item is already in the watchlist, the users are be able to remove it. 
<li>If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).
<li>If the user is signed in and is the one who created the listing, the user have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active. 
<li>Users who are signed in are be able to add comments to the listing page.

### Watchlist:
Users who are signed in are be able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist.

