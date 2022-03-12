from django.forms import ModelForm
from .models import createListingModel, commentModel

class createListingForm(ModelForm):
    class Meta:
        model = createListingModel
        exclude = ['seller', 'active', 'winner']


class commentForm(ModelForm):
    class Meta:
        model = commentModel
        exclude = ['author', 'product']    