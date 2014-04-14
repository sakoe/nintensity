from django.conf.urls import patterns, include, url
from django.contrib import admin
from fitgoals.admin import user_admin_site
from fitgoals.admin import autodiscover as user_site_autodiscover

admin.autodiscover()
user_site_autodiscover(usersite = user_admin_site)

urlpatterns = patterns('',
    url(r'^', include('fitgoals.urls')),
    url(r'^accounts/',
       include('registration.backends.default.urls')),
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'forgot_password.html', 'post_reset_redirect': '/'},
        name="reset_password"),
    url(r'^accounts/password/reset/done/$',
       'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       'django.contrib.auth.views.password_reset_confirm',
       name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
       name='password_reset_complete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(user_admin_site.urls)),
    url(r'^login/$',
       'django.contrib.auth.views.login',
       {'template_name': 'login.html'},
       name="login"),
    url(r'^logout/$',
       'django.contrib.auth.views.logout',
       {'next_page': '/'},
       name="logout"),
    )