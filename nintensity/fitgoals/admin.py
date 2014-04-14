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

from fitgoals.models import WorkoutLog, WorkoutType, Event


class UserAdminAuthenticationForm(AuthenticationForm):

    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput,
                                                initial=1,
                                                error_messages={'required': ugettext_lazy(
                                                    "Please log in again, because your session has"
                                                    " expired.")})

    def clean(self):
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


class UserAdmin(AdminSite):

    """
    Subclass from Django AdminSite
    Overload has_permission function to allow non-staff user to login
    Overload index function to customize index page
    """

    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

    def index(self, request, extra_context=None):
        """
        Customize admin index page
        """
        return (
            super(UserAdmin, self).index(request, extra_context=extra_context)
        )


class WorkoutTypeAdmin(admin.ModelAdmin):

    """
    Customize workout type admin page.
    """

    list_display = (
        'workout_type',
        'has_distance_component',
    )


class WorkoutLogAdmin(admin.ModelAdmin):

    """
    Customize workout log admin page
    """

    list_display = (
        'user',
        'workout_name',
        'workout_type',
        'workout_duration_hours',
        'workout_duration_minutes',
        'workout_distance_miles',
        'workout_date',
        'created_date',
    )
    readonly_fields = ['created_date']

    def queryset(self, request):
        qs = super(WorkoutLogAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(
                username=request.user.username)
        return (
            super(
                WorkoutLogAdmin,
                self).formfield_for_foreignkey(
                db_field,
                request,
                **kwargs)
        )


class EventAdmin(admin.ModelAdmin):

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
