"""
   fitgoals models
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MaxValueValidator
from registration.signals import user_activated


class WorkoutType(models.Model):

    """
    Model to use in the admin control panel to add new workout types.
    """
    workout_type = models.CharField(max_length=128)
    has_distance_component = models.BooleanField()

    def __unicode__(self):
        return self.workout_type


class WorkoutLog(models.Model):

    """
    Model for workout log
    Activity is given as shortname for Workout Name
    Duration is given as shortname for Workout Duration
    Miles is given as shortname for Workout Distance Miles
    Type is given as shortname for Workout Type
    """
    workout_name = models.CharField("Activity", max_length=128)
    workout_duration = models.TimeField("Duration", blank=True)
    workout_distance_miles = models.DecimalField("Miles", max_digits=4, decimal_places=2)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField("Entered on", auto_now_add=True)
    workout_date = models.DateTimeField("Workout Date", blank=True, null=True)
    workout_type = models.ForeignKey('WorkoutType', verbose_name="Type")

    class Meta:
        verbose_name = 'Workout'

    def __unicode__(self):
        return self.workout_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('fitgoals.views.details', args=[str(self.id)])


class Event(models.Model):
    event_name = models.CharField(max_length=128)
    event_description = models.TextField()
    event_date = models.DateTimeField(auto_now=False, null=False)
    event_location = models.CharField(max_length=128)
    event_url = models.URLField(max_length=200)


class Team(Group):

    """
    Model for Team
    """
    team_name = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s' % (self.team_name)


class EventTeam(models.Model):
    event_for_this_team = models.ForeignKey('Event')
    team_for_this_event = models.ForeignKey('Team')


def user_activated_callback(sender, user, request, **kwargs):
    """
    Callback function when activation is complete
    You can update user's permission here.
    Currently, only add/change/delete permission on workoutlog is
    set after activation complete.
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
