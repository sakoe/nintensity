from django.db import models
from django.contrib.auth.models import User

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
        return reverse('people.views.details', args=[str(self.id)])
