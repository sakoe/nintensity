from django.shortcuts import render
from fitgoals.admin import WorkoutLog, WorkoutType, user_admin_site
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from fitgoals.admin import Event, Team, TeamMember
from django import forms


# FUNCTIONS ####################################################################


def team_and_user_info(request, event_pk):
    """
    function that returns multiple values for multiple event views
    """
    # current event's teams are found
    event_teams = Team.objects.filter(event=event_pk).order_by('date_created')

    # list of teams with team name and list of members for each team created
    all_teams_for_event = []
    for each in event_teams:
        complete_team = [each.pk, each.team_name]
        members = TeamMember.objects.filter(team_id=each.pk).order_by('date_joined')
        str_members = []
        for each in members:
            str_members.append(str(each))
        complete_team.append(str_members)
        all_teams_for_event.append(complete_team)

    # current user's info is found
    particular_user = User.objects.get(username=request.user)

    # whether current user has created a team for this event is determined
    user_created_team = Team.objects.filter(team_creator=particular_user.id,
        event_id=event_pk)
    if len(user_created_team) > 0:
        can_make_team = False
    else:
        can_make_team = True

    # whether current user has joined a team for this event is determined
    user_team_memberships_for_event = []
    for each in event_teams:
        memberships = TeamMember.objects.filter(team_id=each.pk, member_id=particular_user.id)
        for each in memberships:
            user_team_memberships_for_event.append(each)
    if len(user_team_memberships_for_event) > 0:
        can_join_team = False
    else:
        can_join_team = True

    return all_teams_for_event, particular_user, can_make_team, can_join_team


# HANDY DATA ###################################################################


# simple dictionary of month names created for use in multiple views
MONTH_NAMES = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May',
               6:'June', 7:'July', 8:'August', 9:'September', 10:'October',
               11:'November', 12:'December'}


# VIEWS ########################################################################


def root_view(request):
    """
    This provides the site's root view
    """
    return render(request, 'root_view.html')


@login_required
def workouts_view(request):
    """
    This provides the site's workouts view
    It uses get_model_admin() method from UserAdmin to
    get the WorkoutLogAdmin object to call its changelist_view directly.
    """
    # return render(request, 'workouts_view.html')
    workoutlog_admin = user_admin_site.get_model_admin(WorkoutLog)
    if workoutlog_admin is None:
        return render(request, 'workouts_view.html')
    else:
        return workoutlog_admin.changelist_view(request)


@login_required
def events_view(request):
    """
    This provides the site's events view
    """
    # if at least one event exists...
    if len(Event.objects.all()) > 0:
        # all events dicovered
        all_events = Event.objects.all().order_by('-event_date')

        # events grouped
        events_group = []
        for year in range(all_events[0].event_date.year, all_events[len(all_events) - 1].event_date.year - 1, -1):
            year_group = []
            for month_num in range(1,13,1):
                month_group = []
                for event in all_events:
                    current_event = []
                    if event.event_date.year == year and event.event_date.month == month_num:
                        current_event.append(event.event_date.year)
                        current_event.append(event.event_date.month)
                        current_event.append(MONTH_NAMES[month_num])
                        current_event.append(event.event_date.day)
                        current_event.append(event.event_name)
                        current_event.append(event.id)
                        current_event.append(event.event_creator)
                        month_group.append(current_event)
                if len(month_group) > 0:
                    month_group = sorted(month_group, key=lambda x: x[3])
                    year_group.append(month_group)
            events_group.append(year_group)

        # current user's info is found
        particular_user = User.objects.get(username=request.user)

        # context is set
        context = {}
        context['events_group'] = events_group
        context['particular_user'] = particular_user
        return render(request, 'events_view.html', context)
    
    # ...but if no events exist
    else:
        # context is set
        context = {}
        return render(request, 'events_view.html', context)


@login_required
def event_year_view(request, event_year):
    """
    This provides the site's event year view
    """
    # years prior to 1902 and after 2102 raise a 404 error
    if int(event_year) < 1902 or int(event_year) > 2102:
        raise Http404

    # year's events are found and sorted
    events_this_year = Event.objects.filter(event_date__year=str(event_year)).order_by('event_date')

    # events are grouped by month
    grouped_monthly_events = []
    for each in range(1,13,1):
        month_group = events_this_year.filter(event_date__month=str(each))
        if len(month_group) < 1:
                continue
        grouping = []
        for each in month_group:
            grouping.append(each)
        with_month = (MONTH_NAMES[grouping[0].event_date.month], grouping)
        grouped_monthly_events.append(with_month)

    # current user's info is found
    particular_user = User.objects.get(username=request.user)

    # context is set
    context = {}
    context['event_year'] = event_year
    context['grouped_monthly_events'] = grouped_monthly_events
    context['particular_user'] = particular_user
    return render(request, 'event_year_view.html', context)


@login_required
def event_details_view(request, event_year, event_pk):
    """
    This provides the site's event details view
    """
    # event (if it exists) is found
    try:
        all_events = Event.objects.all()
        specific_event = all_events.get(event_date__year=event_year, pk=event_pk)
    except Event.DoesNotExist:
        raise Http404

    all_teams_for_event, particular_user, can_make_team, can_join_team = team_and_user_info(request, event_pk)

    # url assesed
    include_url = True if specific_event.event_url else False

    # context is set
    context = {}
    context['event'] = specific_event
    context['all_teams_for_event'] = all_teams_for_event
    context['can_make_team'] = can_make_team
    context['can_join_team'] = can_join_team
    context['particular_user'] = particular_user
    context['username'] = particular_user.username
    context['include_url'] = include_url
    return render(request, 'event_details_view.html', context)


@login_required
def event_delete_view(request, event_year, event_pk):
    """
    This provides the site's event delete view
    """
    # event (if it exists) is found
    try:
        all_events = Event.objects.all()
        specific_event = all_events.get(event_date__year=event_year, pk=event_pk)
    except Event.DoesNotExist:
        raise Http404

    # current user's info is found
    particular_user = User.objects.get(username=request.user)

    # the form being utilized for this view
    CHOICES = (('0', 'Yes',), ('1', 'No',))
    class DeleteEventForm(forms.Form):
        delete_option = forms.ChoiceField(
            initial = '1',
            label = 'Are you absolutely sure you want to delete this event?',
            widget = forms.RadioSelect,
            choices = CHOICES
    )

    # context is set
    context = {}
    context['specific_event'] = specific_event
    context['particular_user'] = particular_user
    context['event_creator'] = specific_event.event_creator

    # form-related
    if request.method == 'POST':
        form = DeleteEventForm(request.POST)
        if form.is_valid():
            delete_option = form.cleaned_data['delete_option']
            if delete_option == '1':
                return HttpResponseRedirect('..')
            elif delete_option == '0':
                # delete event
                specific_event.delete()
                return HttpResponseRedirect('../../..')
        else:
            context['form'] = form
            return render(request, 'event_delete_view.html', context)
    else:
        form = DeleteEventForm()
        context['form'] = form
        return render(request, 'event_delete_view.html', context)


@login_required
def event_join_or_leave_team(request, event_year, event_pk, team_pk):
    """
    This provides the site's event join or leave team view
    """
    # event (if it exists) is found
    try:
        all_events = Event.objects.all()
        specific_event = all_events.get(event_date__year=event_year, pk=event_pk)
    except Event.DoesNotExist:
        raise Http404

    all_teams_for_event, particular_user, can_make_team, can_join_team = team_and_user_info(request, event_pk)

    # specific team found
    for team in all_teams_for_event:
        if int(team_pk) == team[0]:
            specific_team = team

    # 404 raised if bad team_pk manually typed into url
    try:
        x = specific_team
    except UnboundLocalError:
        raise Http404

    # check if user is on this specific team
    on_team = False
    for each in specific_team[2]:
        if each == str(particular_user):
            on_team = True

    # ability to leave/join team is assessed, and appropriate action is taken
    if on_team:
        team_in_question = Team.objects.get(pk=specific_team[0])
        # if user is the team's creator, give option to delete the entire team
        if particular_user.pk == team_in_question.team_creator.pk:
            # redirect to delete team view
            return HttpResponseRedirect('delete-team/')
        # ...otherwise, simply unjoin the user
        else:
            current_member = TeamMember.objects.get(
                team_id=specific_team[0],
                member_id=particular_user.pk
            )
            current_member.delete()
        return HttpResponseRedirect('..')
    elif can_join_team and can_make_team: # if user is not on team, join
        # user added to team
        new_member = TeamMember(
            team_id=team_pk,
            member_id=particular_user.pk
        )
        new_member.save()
        return HttpResponseRedirect('..')
    else:
        # context is set
        context = {}
        context['specific_event'] = specific_event
        context['specific_team'] = specific_team
        context['can_make_team'] = can_make_team
        context['can_join_team'] = can_join_team
        return render(request, 'event_join_team_view.html', context)


@login_required
def event_make_team(request, event_year, event_pk):
    """
    This provides the site's event make team view
    """
    # event (if it exists) is found
    try:
        all_events = Event.objects.all()
        specific_event = all_events.get(
            event_date__year=event_year,
            pk=event_pk
        )
    except Event.DoesNotExist:
        raise Http404

    all_teams_for_event, particular_user, can_make_team, can_join_team = team_and_user_info(request, event_pk)

    # list of current teams for particular event
    teams_list = []
    for each in all_teams_for_event:
        teams_list.append(each[1])

    # the form being utilized for this view
    class MakeTeamForm(forms.Form):
        team_name = forms.CharField(label='New Team Name', max_length=100)

        def clean_team_name(self):
            data = self.cleaned_data['team_name']
            if data in teams_list:
                raise forms.ValidationError("Please select another team name")
            return data

    # context is set
    context = {}
    context['specific_event'] = specific_event
    context['can_make_team'] = can_make_team
    context['can_join_team'] = can_join_team
    context['teams_list'] = teams_list

    # form-related
    if request.method == 'POST':
        if can_make_team == False or can_join_team == False:
            form = MakeTeamForm()
            context['form'] = form
            return render(request, 'event_make_team_view.html', context)
        form = MakeTeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            if team_name in teams_list:
                # return ValidationError message
                context['form'] = form
                return render(request, 'event_make_team_view.html', context)
            else:
                # new team created and user added to team
                new_team = Team(
                    event_id=specific_event.pk,
                    team_name=team_name,
                    team_creator=particular_user
                )
                new_team.save()
                first_member = TeamMember(
                    team_id=new_team.pk,
                    member_id=particular_user.pk
                )
                first_member.save()
                return HttpResponseRedirect('..')
        else:
            context['form'] = form
            return render(request, 'event_make_team_view.html', context)
    else:
        form = MakeTeamForm()
        context['form'] = form
        return render(request, 'event_make_team_view.html', context)


@login_required
def event_delete_team(request, event_year, event_pk, team_pk):
    """
    This provides the site's event delete team view
    """
    # event (if it exists) is found
    try:
        all_events = Event.objects.all()
        specific_event = all_events.get(
            event_date__year=event_year,
            pk=event_pk
        )
    except Event.DoesNotExist:
        raise Http404

    all_teams_for_event, particular_user, can_make_team, can_join_team = team_and_user_info(request, event_pk)
    
    # specific team found
    for team in all_teams_for_event:
        if int(team_pk) == team[0]:
            specific_team = team

    # 404 raised if bad team_pk manually typed into url
    try:
        x = specific_team
    except UnboundLocalError:
        raise Http404

    # whether user is team creator is determined
    team_in_question = Team.objects.get(pk=specific_team[0])
    if particular_user.pk == team_in_question.team_creator.pk:
        team_creator = True
    else:
        team_creator = False

    # the form being utilized for this view
    CHOICES = (('0', 'Yes',), ('1', 'No',))
    class DeleteTeamForm(forms.Form):
        delete_option = forms.ChoiceField(
            initial = '1',
            label = 'Are you absolutely sure you want to dissolve this team?',
            widget = forms.RadioSelect,
            choices = CHOICES
    )

    # context is set
    context = {}
    context['specific_event'] = specific_event
    context['team_creator'] = team_creator

    # form-related
    if request.method == 'POST':
        form = DeleteTeamForm(request.POST)
        if form.is_valid():
            delete_option = form.cleaned_data['delete_option']
            if delete_option == '1':
                return HttpResponseRedirect('../..')
            elif delete_option == '0':
                # delete entire team
                team_in_question.delete()
                return HttpResponseRedirect('../..')
        else:
            context['form'] = form
            return render(request, 'event_delete_team_view.html', context)
    else:
        form = DeleteTeamForm()
        context['form'] = form
        return render(request, 'event_delete_team_view.html', context)

    
@login_required
def leaderboards_view(request):
    """
    This provides the site's leaderboards view
    """
    # current month, current month name and current year are determined
    current_month = datetime.date.today().month
    month_name = MONTH_NAMES[current_month]
    current_year = datetime.date.today().year

    # current workout types determined
    workout_types = WorkoutType.objects.all()
    workout_types_list = []
    for each in workout_types:
        workout_types_list.append((each.id, each.workout_type))

    # current site users determined
    site_users = User.objects.all()

    # user_tallies list is whipped up...
    # lists [username, workout type id, workout type, duration for month(secs)]
    # are placed into lists per user
    # which are placed into a user_tallies list
    user_tallies = []
    for user in site_users:
        user_data = []
        for category in workout_types:
            workout_group = []
            workout_group.append(user.username)
            workout_group.append(category.id)
            workout_group.append(category.workout_type)

            # total duration(secs) for user & workout type determined
            all_workouts = WorkoutLog.objects.all()
            user_workouts = all_workouts.filter(
                user_id=user.id,
                workout_type=category.id,
                workout_date__month=current_month
            )
            
            total_duration = 0
            for each in user_workouts:
                h = each.workout_duration.hour*60*60
                m = each.workout_duration.minute*60
                s = each.workout_duration.second
                total_duration += (h + m + s) 
            
            workout_group.append(total_duration)

            user_data.append(workout_group)
        user_tallies.append(user_data)

    # final list for leaderboards is created
    leaderboards_list = []
    for each in workout_types_list:
        workout_type_grouping = []
        workout_type_grouping.append(each)
        workout_type_grouping.append([])
        leaderboards_list.append(workout_type_grouping)

    for each in leaderboards_list:
        for user_data in user_tallies:
            for workout_group in user_data:
                if workout_group[1] == each[0][0] and workout_group[3] > 0:
                    each[1].append(workout_group)

    for each in leaderboards_list:
        each[1] = sorted(each[1], key=lambda x: x[3], reverse=True)

    for grouping in leaderboards_list:
        if len(grouping[1]) > 0:
            for each in grouping[1]:
                each.append((float(each[3])/float(grouping[1][0][3]))*100)

    # context is set
    context = {}
    context['current_month'] = current_month
    context['month_name'] = month_name
    context['current_year'] = current_year
    context['leaderboards_list'] = leaderboards_list
    return render(request, 'leaderboards_view.html', context)







