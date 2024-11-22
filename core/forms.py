from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'border border-gray-300 rounded-full px-4 w-full text-black'
        })
