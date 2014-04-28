"""
These are unit tests for using the fitgoals module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from fitgoals.models import WorkoutType


class FitGoalsTestCase(TestCase):
    fixtures = ['fitgoals_test_fixture.json', ]

    def setUp(self):
        self.user = User.objects.get(pk=1)


class WorkoutTypeTestCase(TestCase):

    def test_unicode(self):
        expected = "Cycling"
        wt = WorkoutType(workout_type=expected)
        actual = unicode(wt)
        self.assertEqual(expected, actual)
