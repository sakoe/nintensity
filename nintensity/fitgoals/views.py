from django.shortcuts import render

"""
.. module:: views
   :platform: Unix
   :synopsis: define views for gitgoals

"""

def goals_view(request):
    """ This provides goals view
    """
    return render(request, 'goals.html')
