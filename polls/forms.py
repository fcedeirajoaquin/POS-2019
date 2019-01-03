from django import forms
from django.forms import ModelForm, CharField, TextInput
class NameForm(forms.Form):
    your_name = forms.CharField(label='',min_length=5, max_length=8,widget=TextInput(attrs={'class':'form-control','pattern':'[0-9]+','min_value':'1000' ,'title':'Ingrese solo numeros.'}))
# 	your_name = forms.CharField(label='',min_length=5, max_length=8, widget=TextInput(attrs={'class':'form-control','autocomplete': 'off','pattern':'[0-9]+', 'title':'Ingrese solo numeros.'}))
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()