from django import forms
from .models import ProfilePicture
from home.models import Product

#form to update / create a profile picture
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ('image',)

class AddListingForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("created_at",)
       