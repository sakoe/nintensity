from django.shortcuts import render
from fitgoals.admin import WorkoutLog, user_admin_site

"""

"""

def root_view(request):
    """
    This provides the site's root view
    """
    return render(request, 'root_view.html')

def profile_view(request):
    """
    This provides the site's profile view
    """
    return render(request, 'profile_view.html')

def workouts_view(request):
    """
    This provides the site's workouts view
    """
    #return render(request, 'workouts_view.html')
    workoutlog_admin = user_admin_site.get_model_admin(WorkoutLog)   
    if workoutlog_admin is None:
        return render(request, 'workouts_view.html')
    else:
        return workoutlog_admin.changelist_view(request)

def events_view(request):
    """
    This provides the site's events view
    """
    return render(request, 'events_view.html')

def leaderboards_view(request):
    """
    This provides the site's leaderboardss view
    """
    return render(request, 'leaderboards_view.html')
