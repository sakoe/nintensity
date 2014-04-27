from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fitbit_id = models.CharField(max_length=128)
    runkeeper_id = models.CharField(max_length=128)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

