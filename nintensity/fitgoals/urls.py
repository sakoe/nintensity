from django.conf.urls import patterns, url

urlpatterns = patterns('fitgoals.views',
    url(r'^$',
        'goals_view',
        name="goals_index"),
)

