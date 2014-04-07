from django.shortcuts import render

"""

"""

def root_view(request):
    """ This provides the site's root view
"""
    return render(request, 'root_view.html')