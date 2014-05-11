"""fitgoals admin

   custom admin site for fitgoal users

"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite, site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.forms import ERROR_MESSAGE
from django import forms
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.shortcuts import redirect
from fitgoals.models import WorkoutLog, WorkoutType, Event
from fitgoals.models import Team, TeamMember

class UserAdminAuthenticationForm(AuthenticationForm):

    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff. The main modifications is to
    remove check for staff in clean() function
    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput,
                                                initial=1,
                                                error_messages={'required': ugettext_lazy(
                                                    "Please log in again, because your session has"
                                                    " expired.")})

    def clean(self):
        """
        Replace check for staff with active only
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data


class FitGoalsModelAdmin(admin.ModelAdmin):

    """
    Simple extention to ModelAdmin to jave different default actions.
    """

    def get_action_choices(self, request, default_choices=[]):
        """
        Return a list of choices for use in a form object.  Each choice is a
        tuple (name, description).

        Reset the default_choices to empty list instead of BLANK_CHOICE_DASH
        """
        return (
            super(
                FitGoalsModelAdmin,
                self).get_action_choices(
                request,
                default_choices=default_choices)
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Overload the super class function to limit the display set to
        logined user only.
        """
        if db_field.name == 'user' or 'creator' in db_field.name:
            kwargs['queryset'] = User.objects.filter(
                username=request.user.username)
        return (
            super(
                FitGoalsModelAdmin,
                self).formfield_for_foreignkey(
                db_field,
                request,
                **kwargs)
        )


class UserAdmin(AdminSite):

    """
    Subclass from Django AdminSite
    It uses new login, index and app_index templates that are
    customized for fitgoals.
    Overload has_permission function to allow non-staff user to login
    Overload index function to customize index page
    """

    login_form = UserAdminAuthenticationForm
    login_template = 'admin/fitgoals/login.html'
    index_template = 'admin/fitgoals/index.html'
    app_index_template = 'admin/fitgoals/app_index.html'

    def get_model_admin(self, model):
        """
        find registered model or return none
        """
        return self._registry.get(model)

    def has_permission(self, request):
        """
        Removed check for is_staff. It return true for activated user.
        """
        return request.user.is_active

    def index(self, request, extra_context=None):
        """
        Customize admin index page
        Set the title to "My Fitgoals"
        """
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = 'My Fitgoals'
        return (
            super(UserAdmin, self).index(request, extra_context=extra_context)
        )


class WorkoutTypeAdmin(FitGoalsModelAdmin):

    """
    Customize workout type admin page.
    """

    list_display = (
        'workout_type',
        'has_distance_component',
    )

from django.contrib.admin.widgets import AdminTimeWidget


class DurationTimeForm(forms.ModelForm):

    """
    Customize input form for workout duration field
    set 'class' in attrs of AdminTimeWidget to None to remove time shortcut
    """
    workout_duration = forms.TimeField(
        widget=AdminTimeWidget(format='%H:%M', attrs={'class': 'None'}),
        help_text='Please use the following format: <em>hh:mm</em>.')

    class Meta:
        model = WorkoutLog


class WorkoutLogAdmin(FitGoalsModelAdmin):

    """
    Customize workout log admin page
    It uses its own template to display total workout hours
    """

    form = DurationTimeForm
    list_display = (
        'workout_name',
        'workout_type',
        'format_duration',
        'workout_date',
    )
    readonly_fields = ['created_date']
    change_list_template = 'admin/fitgoals/workoutlog_list.html'

    def changelist_view(self, request, extra_context=None):
        """
        Overload the super ModelAdmin class for changelist_view
        It provides extra for display total workout hours and mins.
        """
        workoutlog_extra = {'total': self.get_total_workout(request)}
        return (
            super(
                WorkoutLogAdmin,
                self).changelist_view(
                request,
                extra_context=workoutlog_extra)
        )

    def get_total_workout(self, request):
        """
        New function added to compute total hours and mins for the logined
        user. It returns a dictionary with Hours and Minutes as keys.
        """
        total_time = WorkoutLog.objects.filter(
            user=request.user).aggregate(tot=Sum('workout_duration'))['tot']
        total_seconds = 0
        if total_time is not None:
            total_seconds = total_time.total_seconds()
        hours = divmod(total_seconds, 3600)
        mins = divmod(hours[1], 60)[0]
        return {'Hours': hours[0], 'Minutes': mins}

    def queryset(self, request):
        """
        Overload the super class function to limit the display set to
        logined user only.
        """
        qs = super(WorkoutLogAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        """
        Overload the parent class and set the inital value
        for user selections to logined user.
        """
        form = super(WorkoutLogAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    def format_duration(self, obj):
        """
        Set the workout_duration to display without a.m.
        It uses the fact that workout_duration is a Python date.time object
        Since we changed from workout_duration, the short_descrption needs update
        """
        return obj.workout_duration.strftime('%H:%M')
    format_duration.short_description = 'Duration'


class EventAdmin(FitGoalsModelAdmin):

    """
    Customize the event admin page.

    """

    list_display = (
        'event_name',
        'event_url',
        'event_date',
        'event_description',
        'event_location',
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Overload the parent class and set the inital value
        for user selections to logined user.
        """
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['event_creator'].initial = request.user
        return form

    def changelist_view(self, request, extra_context=None):
        return redirect('fitgoals.views.events_view')

class TeamAdmin(admin.ModelAdmin):

    """
    Customize the event admin page.

    """

    list_display = (
        'event',
        'team_name',
        'team_creator',
    )


def autodiscover(usersite=site):
    """
    improved autodiscover function from django.contrib.admin
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        try:
            before_import_registry = copy.copy(usersite._registry)
            import_module('%s.admin' % app)
        except:
            usersite._registry = before_import_registry
            if module_has_submodule(mod, 'admin'):
                raise


user_admin_site = UserAdmin(name='user')
user_admin_site.register(WorkoutLog, WorkoutLogAdmin)
user_admin_site.register(Event, EventAdmin)

# admin.site.register(WorkoutLog, WorkoutLogAdmin)
admin.site.register(WorkoutType, WorkoutTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Team, TeamAdmin)
