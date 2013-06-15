from django.conf.urls import patterns, include, url
from ian import view

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ian.views.home', name='home'),
    # url(r'^ian/', include('ian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^firstresponse/$',view.firstresponse,name='firstresponse'),
    url(r'^firstpage/$',view.firstpage,name='firstpage')
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
