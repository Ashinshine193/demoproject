from django import forms
from django.contrib.auth.models import User


class Register_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=12, min_length=5)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=12, min_length=5)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password','confirm_password','email')