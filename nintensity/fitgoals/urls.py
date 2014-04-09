from django.conf.urls import patterns, url

urlpatterns = patterns('fitgoals.views',
    url(r'^$',
        'root_view',
        name='root_view'),
    url(r'^teams/',
        'teams_view',
        name='teams_view'),
    url(r'^events/',
        'events_view',
        name='events_view'),
)