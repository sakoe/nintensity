"""
   fitgoals models
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MaxValueValidator
from registration.signals import user_activated




class WorkoutLog(models.Model):
    """
    Model for workout log
    """
    workout_name = models.CharField(max_length=128)
    workout_units = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    workout_date = models.DateTimeField(blank=True, null=True)
    workout_type = models.IntegerField(validators=[MaxValueValidator(15)]) # cChange this number if the number of workout types changes.


    def __unicode__(self):
        return self.workout_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('fitgoals.views.details', args=[str(self.id)])

    


class Team(Group):
    """
    Model for workout log
    """
    def __unicode__(self):
        return u'%s' % (self.name)


def user_activated_callback(sender, user, request, **kwargs):
    """
    Callback function when activation is complete
    You can update user's permission
    """
    profile = WorkoutLog(user=user)
    team, created = Team.objects.get_or_create(name='Soccer')
    user.groups.add(team)

    perm = Permission.objects.get(codename='add_workoutlog')
    user.user_permissions.add(perm)
    perm = Permission.objects.get(codename='change_workoutlog')
    user.user_permissions.add(perm)
    perm = Permission.objects.get(codename='delete_workoutlog')
    user.user_permissions.add(perm)
    user.save()

user_activated.connect(user_activated_callback)
