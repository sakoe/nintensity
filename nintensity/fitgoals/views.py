from django.shortcuts import render

"""

"""

def root_view(request):
    """
    This provides the site's root/profile view
    """
    context = {'active': 'Root'}
    return render(request, 'root_view.html', context)

def workouts_view(request):
    """
    This provides the site's workouts view
    """
    context = {'active': 'Workouts'}
    return render(request, 'workouts_view.html', context)

def events_view(request):
    """
    This provides the site's events view
    """
    context = {'active': 'Events'}
    return render(request, 'events_view.html', context)

def leaderboards_view(request):
    """
    This provides the site's leaderboardss view
    """
    context = {'active': 'Leaderboards'}
    return render(request, 'leaderboards_view.html', context)