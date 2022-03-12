
from auctions.models import User, createListingModel, watchlistModel, bidModel, commentModel
from django.contrib import admin


admin.site.register(User)
admin.site.register(createListingModel)
admin.site.register(watchlistModel)
admin.site.register(bidModel)
admin.site.register(commentModel)
