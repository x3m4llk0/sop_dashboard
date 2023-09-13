from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, all_sop, all_role
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите лолин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))
    class Meta:
        model = User
        fields = ('username', 'password')    #может быть и [,]

class UserRegistrationForm(UserCreationForm):
    user_id = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Введите Telegram ID'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Введите фамилию'}))
    sop = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-select'}), choices=all_sop)
    role = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-select'}), choices=all_role)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Введите логин'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Введите пароль' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Подтвердите пароль' }))


    class Meta:
        model = User

        fields = ('user_id', 'first_name', 'last_name', 'username', 'password1', 'password2', 'access', 'sop', 'role',)