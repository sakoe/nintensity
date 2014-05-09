from django.shortcuts import render
from fitgoals.admin import WorkoutLog, user_admin_site
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from fitgoals.admin import Event, Team, TeamMember
from django import forms


# FUNCTIONS


def event_grouper(timely_events):
    """
    function wherein future/past events are grouped by year for the events_view
    """
    grouped_events = []
    for each in range(timely_events[0].event_date.year,
        timely_events[len(timely_events) - 1].event_date.year - 1, -1):
        year_group = timely_events.filter(event_date__year=str(each))
        if len(year_group) < 1:
            continue
        grouping = []
        for each in year_group:
            grouping.append(each)
        grouped_events.append(grouping)
    return grouped_events


def final_grouper(timely_group):
    """
    function wherein future/past events are regrouped by year (with subgroups by
    month) for the events_view
    """
    final_grouping = []
    for year in timely_group:
        year_grouping = []
        for each in range(12,0,-1):
            year_month_group = [year[0].event_date.year, month_names[each]]
            for event in year:
                if each == event.event_date.month:
                    year_month_group.append(event)
            if len(year_month_group) > 2:
                if year_month_group[0] == year[0].event_date.year:
                    year_grouping.append(year_month_group)
        final_grouping.append(year_grouping)
    return final_grouping


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


# HANDY DATA


# simple dictionary of month names created for use in multiple views
month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May',
               6:'June', 7:'July', 8:'August', 9:'September', 10:'October',
               11:'November', 12:'December'}


################################################################################


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
        # all events are grouped and sorted in reverse chronological order
        all_events = Event.objects.all().order_by('-event_date')
        
        # future events group is formed
        future_events = all_events.exclude(event_date__lte=datetime.date.today())

        # past events group is formed
        past_events = all_events.exclude(event_date__gte=datetime.date.today())

        if len(future_events) > 0:
            future_grouping = final_grouper(event_grouper(future_events))
        else:
            future_grouping = []
        
        if len(past_events) > 0:
            past_grouping = final_grouper(event_grouper(past_events))
        else:
            past_grouping = []

        # context is set
        context = {}
        context['future_grouping'] = future_grouping
        context['past_grouping'] = past_grouping
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
    events_this_year = Event.objects.filter(event_date__year=str(event_year)).order_by('-event_date')

    # events are grouped by month
    grouped_monthly_events = []
    for each in range(12,0,-1):
        month_group = events_this_year.filter(event_date__month=str(each))
        if len(month_group) < 1:
                continue
        grouping = []
        for each in month_group:
            grouping.append(each)
        with_month = (month_names[grouping[0].event_date.month], grouping)
        grouped_monthly_events.append(with_month)

    # context is set
    context = {}
    context['event_year'] = event_year
    context['grouped_monthly_events'] = grouped_monthly_events
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
    if specific_event.event_url:
        include_url = True
    else:
        include_url = False

    # context is set
    context = {}
    context['event'] = specific_event
    context['all_teams_for_event'] = all_teams_for_event
    context['can_make_team'] = can_make_team
    context['can_join_team'] = can_join_team
    context['username'] = particular_user.username
    context['include_url'] = include_url
    return render(request, 'event_details_view.html', context)


@login_required
def event_join_or_leave_team(request, event_year, event_pk, team_pk):
    """
    This provides the site's event 'join or leave team' view
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
        # if user is the team's creator, delete the team and unjoin all users
        # from team...
        if particular_user.pk == team_in_question.team_creator.pk:
            # delete entire team
            team_in_question.delete()
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
def event_make_team(request, event_year, event_pk, action):
    """
    This provides the site's event "make team" view
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
                # ERROR MESSAGE NEEDED WHEN NAME IS ALREADY TAKEN ##############
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
def leaderboards_view(request):
    """
    This provides the site's leaderboards view
    """
    return render(request, 'leaderboards_view.html')
