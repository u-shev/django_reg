from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        email = forms.EmailField(required=True)
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password1', 'password2')


class UserUpdateForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')


class EmailChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', )
