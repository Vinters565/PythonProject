from django import forms

class AddDateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'name': 'date'}), label='Дата')
