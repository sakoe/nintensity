from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    """
    Gets the user profile information if it exists and allows user to update it.
    Creates a new profile for the logged in user if none exists.
    Displays error messages for fields that are not valid.

    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
        else: 
            args = {}
            args.update(csrf(request))
            args['form'] = form
            return render(request,'profile.html', args) 
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

        args = {}
        args.update(csrf(request))

        args['form'] = form

        return render(request, 'profile.html', args)