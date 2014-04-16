from django.shortcuts import render

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
    return render(request, 'workouts_view.html')

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