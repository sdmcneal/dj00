from django.conf.urls import patterns, url
from gps.views import TrackCreate, TrackUpdate, TrackDelete
from gps import views

urlpatterns = patterns('',
                       url(r'^add/$',views.index,name='index'),
                       url(r'^addplace/$',views.add_place,name='add_place'),
                       url(r'^howfar/$',views.how_far,name='how_far'),
                       url(r'^entry/$',TrackCreate.as_view(),name='track_add'),
                       url(r'^showform/$',views.entry,name='entry'),
                       url(r'^map/$',views.map,name='map'),
                       url(r'^maplast/$',views.maplast,name='maplast'),
                       url(r'^bingmap/$',views.bingmap,name='bingmap'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       url(r'^cc/$',views.cc,name='cc')
                       )

