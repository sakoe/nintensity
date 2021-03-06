"""
   fitgoals models
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MaxValueValidator
from registration.signals import user_activated
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

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
    """
    Model for fitgoals Events
    """
    event_name = models.CharField(max_length=100, unique=True)
    event_description = models.TextField(blank=True)
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=150)
    event_url = models.URLField(blank=True)
    event_creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.event_name


class Team(models.Model):
    """
    Model for fitgoals Teams
    """
    event = models.ForeignKey(Event)
    team_name = models.CharField(max_length=100)
    team_creator = models.ForeignKey(User)
    date_created = models.DateTimeField('Date Joined', auto_now_add=True)

    class Meta:
        unique_together = ('event', 'team_name')

    def __unicode__(self):
        return self.team_name


class TeamMember(models.Model):
    """
    Model for fitgoals Team Members (NOT for display in Django Admin)
    """
    team = models.ForeignKey(Team)
    member = models.ForeignKey(User)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)

    class Meta:
        unique_together = ('team', 'member')

    def __unicode__(self):
        return str(self.member)


def user_activated_callback(sender, user, request, **kwargs):
    """
    Callback function when activation is complete
    You can update user's permission here.
    Currently, only add/change/delete permission on workoutlog is
    set after activation complete.
    """
    profile = WorkoutLog(user=user)
    group, created = Group.objects.get_or_create(name=settings.DEFAULT_GROUP_NAME)
    user.groups.add(group)
    if created:
        logger.error('It should not be created here!')
    user.save()

user_activated.connect(user_activated_callback)
