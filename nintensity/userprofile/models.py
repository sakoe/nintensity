from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Model for the user profile information.
    """

    user = models.OneToOneField(User)
    screen_name = models.CharField(max_length=35, help_text='Supply a screen name if you want to go by a name other than your username.')
    MALE = 'M'
    FEMALE = 'F'
    DECLINE_TO_STATE = "X"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (DECLINE_TO_STATE, "Don't know/Don't want you to know")
        )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=DECLINE_TO_STATE, 
        help_text='Indicate your gender if you want to be included in gender-specific leaderboards.')
    fitbit_id = models.CharField(max_length=128)
    runkeeper_id = models.CharField(max_length=128)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

