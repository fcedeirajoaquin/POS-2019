from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Tu nombre', max_length=100)