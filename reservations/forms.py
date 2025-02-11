from django import forms


class ReserVationForm(forms.Form):
    date = forms.SelectDateWidget()
    field = forms.Select()
