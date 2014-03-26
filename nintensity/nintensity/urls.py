from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nintensity.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('fitgoals.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', #include('registration.backends.default.urls'),
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name="login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name="logout"),

)
