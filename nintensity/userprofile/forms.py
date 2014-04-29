from django import forms
from models import UserProfile

class UserProfileForm(forms.ModelForm):
    

    class Meta:
        model = UserProfile
        fields = ('screen_name','gender','fitbit_id','runkeeper_id')