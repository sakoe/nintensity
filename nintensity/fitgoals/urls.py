from django.conf.urls import patterns, url

urlpatterns = patterns('fitgoals.views',
    url(r'^$',
        'root_view',
        name='root_view'),
    url(r'^profile/$',
        'profile_view',
        name='profile_view'),
    url(r'^workouts/$',
        'workouts_view',
        name='workouts_view'),
    url(r'^events/$',
        'events_view',
        name='events_view'),
    url(r'^leaderboards/$',
        'leaderboards_view',
        name='leaderboards_view'),
)