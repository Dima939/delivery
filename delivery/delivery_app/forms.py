from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    phone = forms.CharField(label='Телефон', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(), disabled=True)
    email = forms.CharField(label='E-mail', widget=forms.TextInput(), disabled=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone']


class OrderForm(forms.Form):
    address = forms.CharField(label='Адрес', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    is_bonus = forms.BooleanField(required=False)
