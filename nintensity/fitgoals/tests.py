"""
These are unit tests for using the fitgoals module.
"""
import datetime
from django.test import TestCase
from django.utils.timezone import utc
from django.contrib.auth.models import User
from fitgoals.models import WorkoutType, WorkoutLog


class FitGoalsTestCase(TestCase):

    """
    The base class for FitGoals TestCase
    It loads the fixture and login the test user.
    """
    fixtures = ['fitgoals_test_fixture.json', ]

    def setUp(self):
        """
        Login as test user
        """
        self.user = User.objects.get(pk=2)
        self.logged_in = self.client.login(
            username=self.user.username,
            password='test1')


class WorkoutTypeTestCase(TestCase):

    """
    This test case directly subclass from django TestCase
    It tests WorkoutType unicode
    """

    def test_unicode(self):
        expected = "Cycling"
        wt = WorkoutType(workout_type=expected)
        actual = unicode(wt)
        self.assertEqual(expected, actual)


class WorkoutLogTestCase(FitGoalsTestCase):

    """
    This test case for WorkoutLog, subclass from FitGoalsTestCase
    It tests WorkoutLog
    """

    def setUp(self):
        """
        Call parent setUp to login as test user
        Add Cycling Excercise workout log
        Duration is 30 mins
        Save the workout
        """
        super(WorkoutLogTestCase, self).setUp()
        wt = WorkoutType.objects.get(pk=3)
        wl = WorkoutLog(workout_name='Cycling Excercise', user=self.user,
                        workout_distance_miles=0.00, workout_type=wt,
                        workout_duration=datetime.time(0, 30))
        wl.save()

    def test_workoutlog(self):
        """
        Test workout view
        Test Cycling Excercise is saved
        Test calculation of Total workout time for hours and minutes
        """
        resp = self.client.get('/workouts/')
        self.assertContains(resp, 'Cycling Excercise')
        self.assertContains(resp, 'Total workout time:')
        self.assertContains(resp, 'Hours - 0.0')
        self.assertContains(resp, 'Minutes - 30.0')
