"""
   management
"""

from django.db.models.signals import post_syncdb
from django.conf import settings
from django.contrib.auth.models import Group, Permission
import fitgoals.models

def create_fitgoal_group(sender, **kwargs):
    """
    create default group
    """
    group, created = Group.objects.get_or_create(name=settings.DEFAULT_GROUP_NAME)
    if created:
	plist = ['add_workoutlog', 'change_workoutlog', 'delete_workoutlog',
		 'add_teammember', 'change_teammember', 'delete_teammember',
		 'add_event', 'change_event', 'delete_event',
		 'add_team', 'change_team', 'delete_team']
	for p in plist:
	    perm = Permission.objects.get(codename=p)
            group.permissions.add(perm)
        group.save()

post_syncdb.connect(create_fitgoal_group, sender=fitgoals.models)
