"""
These are unit tests for using the fitgoals module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from fitgoals.models import WorkoutType, WorkoutLog


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

class WorkoutLogTestCase(FitGoalsTestCase):

    def setUp(self):
        super(WorkoutLogTestCase,self).setUp()
        self.user = User.objects.get(pk=2)
        wl = WorkoutLog(workout_name='Cycling Excercise', user = self.user)
        wl.save()

    def test_workoutlog(self):
        
