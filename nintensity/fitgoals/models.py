"""
   fitgoals models
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MaxValueValidator
from registration.signals import user_activated



class WorkoutType(models.Model):
    """
    Model to use in the admin cotrol panel to add new workout types.
    """
    workout_type = models.CharField(max_length=128)
    has_distance_component = models.BooleanField()

    def __unicode__(self):
        return self.workout_type

class WorkoutLog(models.Model):
    """
    Model for workout log
    """
    workout_name = models.CharField(max_length=128)
    workout_duration_hours = models.IntegerField()
    workout_duration_minutes = models.IntegerField()
    workout_distance_miles = models.IntegerField()
    user = models.ForeignKey(User) # how do we get this to default to the logged-in user?
    created_date = models.DateTimeField(auto_now_add=True)
    workout_date = models.DateTimeField(blank=True, null=True)
    workout_type = models.ForeignKey('WorkoutType')


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
