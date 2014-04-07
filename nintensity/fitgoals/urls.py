from django.conf.urls import patterns, url

urlpatterns = patterns('fitgoals.views',
    url(r'^$',
        'root_view',
        name="site_index"),
)