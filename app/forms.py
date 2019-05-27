from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import Announcement, Person
from django.contrib.auth.models import User


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('price', 'district', 'distance_to_metro', 'area', 'repairs', 'comment')
        labels = {'price': 'Цена'}


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2')
'''
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if 
'''

