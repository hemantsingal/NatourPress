from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mendialdea.views.home', name='home'),
    # url(r'^mendialdea/', include('mendialdea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^feeds/$', 'natourpress.views.feedList'),
    url(r'^feed_detail/(?P<feed_id>\d+)/$', 'natourpress.views.feedDetail'),
    url(r'^addfeed/$', 'natourpress.views.newFeed'),
    url(r'^delete_feed/(?P<feed_id>\d+)/$', 'natourpress.views.deleteFeed'),
    url(r'^author', 'natourpress.views.authorlist'),
    url(r'^tags', 'natourpress.views.taglist'),
    url(r'^npauthor', 'natourpress.views.npauthorlist'),
    url(r'^nptag', 'natourpress.views.nptaglist'),
    url(r'^newnpauthor', 'natourpress.views.newnpauthor'),
    url(r'^newnptag', 'natourpress.views.newnptag'),
    url(r'^setnpauthor', 'natourpress.views.setnpauthor'),
    url(r'^setnptag', 'natourpress.views.setnptag'),
    url(r'^setkarma', 'natourpress.views.setkarma'),
   # url(r'^login', 'natourpress.views.my_login'),
    (r'^login', 'django.contrib.auth.views.login',{'template_name': 'natourpress/login.html'}),
    (r'^logout', 'natourpress.views.logout_view'),
)
