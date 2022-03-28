from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(min_length=13, max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)
