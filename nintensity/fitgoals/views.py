from django.shortcuts import render

"""

"""

def root_view(request):
    """
    This provides the site's root view
    """
    if len(request.path) <= 1:
        context = {'active': 'Root'}
    return render(request, 'root_view.html', context)

def users_view(request):
    """
    This provides the site's users view
    """
    if 'users' in request.path:
        context = {'active': 'Users'}
    return render(request, 'users_view.html', context)

def teams_view(request):
    """
    This provides the site's teams view
    """
    if 'teams' in request.path:
        context = {'active': 'Teams'}
    return render(request, 'teams_view.html', context)

def events_view(request):
    """
    This provides the site's events view
    """
    if 'events' in request.path:
        context = {'active': 'Events'}
    return render(request, 'events_view.html', context)