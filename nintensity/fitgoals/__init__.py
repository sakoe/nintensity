"""fitgoals app

.. moduleauthor:: Gary Pei

"""

from django.db.models.signals import post_syncdb
from django.conf import settings
from django.contrib.auth.models import Group, Permission
import models
from models import WorkoutLog

def create_fitgoal_group(sender, **kwargs):
    """
    create default group
    """
    group, created = Group.objects.get_or_create(name=settings.DEFAULT_GROUP_NAME)

post_syncdb.connect(create_fitgoal_group, sender=models)
