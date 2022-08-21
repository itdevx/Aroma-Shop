from django import forms


class UserNewOrderForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    count = forms.IntegerField(widget=forms.NumberInput(), initial=1)
    