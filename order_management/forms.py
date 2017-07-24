from django import forms

class ConfirmPaymentForm(forms.Form):
    date = forms.DateField
    file = forms.FileField()