from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import datetime


## registrieren
class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD') # für profil
    vorname = forms.CharField(help_text='Required.')
    name = forms.CharField(help_text='Required.')
    email = forms.CharField(help_text='Required.')

    class Meta:
        model = User
        fields = ('vorname', 'name','email', 'username', 'birth_date', 'password1', 'password2', )

CHOICES = [('Buy','Buy'),  ('Sell','Sell')]


## Login
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password' )


## Handelsseite
class TradeForm(forms.Form):
    Art = forms.CharField(max_length=4, widget=forms.Select(choices=CHOICES),)
    Menge   = forms.FloatField(required=False)
    Preis = forms.FloatField(required=False )


## Handelsseite
class PlanForm(forms.Form):
    Preis = forms.FloatField(required=False )
    Tag = forms.IntegerField(required=True )



## Handelsseite
class PlanTagForm(forms.Form):
    Tag = forms.IntegerField(required=True )