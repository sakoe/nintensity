from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def user_profile(request):
    """
Gets the user profile information if it exists and allows user to update it.
Creates a new profile for the logged in user if none exists.
Displays a flash message on successful updates.

"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
        else: # temp "fix" until Sako fixes blank field submission problem
            return HttpResponseRedirect('') # temp "fix" until Sako fixes blank field submission problem
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

        args = {}
        args.update(csrf(request))

        args['form'] = form

        return render(request, 'profile.html', args)