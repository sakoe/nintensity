from django.db import models
from django.contrib.auth.models import User, Group
from registration.signals import user_activated


class WorkoutLog(models.Model):
    workout_name = models.CharField(max_length=128)
    workout_units = models.TextField(blank=True)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    workout_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.workout_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('fitgoals.views.details', args=[str(self.id)])


class Team(Group):
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


def user_activated_callback(sender, user, request, **kwargs):
    profile = WorkoutLog(user=user)
    team, created = Team.objects.get_or_create(name='Soccer')
    user.groups.add(team)

user_activated.connect(user_activated_callback)
