from random import choices
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.encoding import force_str as force_unicode

from .models import Tag, Expense


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'overflow-hidden shadow appearance-nonebg-inherit border rounded w-full bg-inherit py-2 px-3 text-neutral-900 dark:text-white leading-tight focus:outline-none focus:shadow-outline'
            })
        }


class NewExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['type', 'tag', 'amount', 'date', 'description']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'w-full h-full m-0 dark:text-white dark:bg-neutral-900'
            }),
            'tag': forms.Select(attrs={
                'class': 'dark:text-white dark:bg-neutral-900'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'dark:text-white dark:bg-neutral-900'
            }),
            'date': forms.DateInput(attrs={
                'class': 'dark:text-white dark:bg-neutral-900'
            }),
            'description': forms.TextInput(attrs={
                'class': 'dark:text-white dark:bg-neutral-900'
            })
        }

    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = self.fields['tag'].queryset.filter(
            user=current_user)
