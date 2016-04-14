from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'musicon.views.login'),
    url(r'^accounts/auth/$', 'musicon.views.auth_view'),
    url(r'^accounts/loggedin/$', 'musicon.views.loggedin'),
    url(r'^accounts/invalid_login/$', 'musicon.views.invalid_login'),
    url(r'^accounts/logout/$', 'musicon.views.logout'),
    url(r'^accounts/register/$', 'musicon.views.register_user'),
    url(r'^accounts/register_success/$', 'musicon.views.register_success'),

    url(r'^$', 'musicon.views.events'),
    url(r'^search/$', 'musicon.views.search'),
    url(r'^add_fav_event/$', 'musicon.views.add_fav_event'),
    url(r'^add_fav_venue/$', 'musicon.views.add_fav_venue'),
    url(r'^fav_event/$', 'musicon.views.fav_event'),
    url(r'^fav_venue/$', 'musicon.views.fav_venue'),
)
