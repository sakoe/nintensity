from django.shortcuts import render

"""

"""

def root_view(request):
    """
    This provides the site's root view
    """
    return render(request, 'root_view.html')

def teams_view(request):
    """
    This provides the site's teams view
    """
    return render(request, 'teams_view.html')

def events_view(request):
    """
    This provides the site's events view
    """
    return render(request, 'events_view.html')