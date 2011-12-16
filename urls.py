from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NatourPress.views.home', name='home'),
    # url(r'^NatourPress/', include('NatourPress.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^config/', include('natourpress.urls')),
    url(r'^admin/', include(admin.site.urls)),
   # url(r'^login', 'natourpress.views.my_login'),
    url(r'^login', 'django.contrib.auth.views.login',{'template_name': 'natourpress/login.html'}),
    url(r'^logout', 'natourpress.views.logout_view'),
)
