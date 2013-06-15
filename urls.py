from django.conf.urls import patterns, include, url


from django.contrib import admin
#from dj00 import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gps/',include('gps.urls')),
    url(r'^ian/',include('ian.urls'))
    #url(r'^dj/',views.index,name='index')
)