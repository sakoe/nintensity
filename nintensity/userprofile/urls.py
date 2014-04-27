from django.conf.urls import patterns, include, url

urlpatterns = patterns('userprofile.views',
    url(r'^profile/$', 
        'user_profile',
        name='user_profile'),
    )