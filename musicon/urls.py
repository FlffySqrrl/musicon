from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'musicon.views.events'),
    url(r'^search/$', 'musicon.views.search'),
    url(r'^add_fav_event/$', 'musicon.views.add_fav_event'),
    url(r'^add_fav_venue/$', 'musicon.views.add_fav_venue'),
    url(r'^myevents/$', 'musicon.views.disp_fav_events'),
    url(r'^myvenues/$', 'musicon.views.disp_fav_venues'),
    url(r'^accounts/signup/$', 'musicon.views.signup'),
    url(r'^accounts/signin/$', 'musicon.views.signin'),
    url(r'^accounts/signout/$', 'musicon.views.signout'),
)
