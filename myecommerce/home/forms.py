from django import forms

class ItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
