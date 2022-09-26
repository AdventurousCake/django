from django import forms
from django.contrib import admin

from Anketa.models import UserAccount


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = '__all__'

        # for increase charfield
        widgets = {
            'user_anketa_data': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }

        exclude = ['mobile_number', 'email', 'city', 'country', 'full_name', 'updated_date']


