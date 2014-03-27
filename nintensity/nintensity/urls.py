from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('fitgoals.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
#    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'forgot_password.html',\
#    'post_reset_redirect' : '/'}, name="reset_password"),
#    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name="login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name="logout"),

)
