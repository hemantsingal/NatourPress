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
    url(r'^addlayout/$', 'natourpress.views.newLayout'),
    url(r'^addsubplace/$', 'natourpress.views.addSubPlace'),
    url(r'^layout_detail/(?P<layout_id>\d+)/$', 'natourpress.views.layoutDetail'),
    url(r'^subplace_detail/(?P<subplace_id>\d+)/$', 'natourpress.views.subplaceDetail'),
    url(r'^topic_detail/(?P<topic_id>\d+)/$', 'natourpress.views.topicDetail'),
    url(r'^cell_detail/(?P<cell_id>\d+)/$', 'natourpress.views.cellDetail'),
    url(r'^delete_feed/(?P<feed_id>\d+)/$', 'natourpress.views.deleteFeed'),
    url(r'^delete_layout/(?P<layout_id>\d+)/$', 'natourpress.views.deleteLayout'),
    url(r'^author/$', 'natourpress.views.authorlist'),
    url(r'^tags/$', 'natourpress.views.taglist'),
    url(r'^addtopic/$', 'natourpress.views.addTopic'),
    url(r'^selectcategory/$', 'natourpress.views.selectCategory'),
    url(r'^addcell/$', 'natourpress.views.addCell'),
    url(r'^npauthor/$', 'natourpress.views.npauthorlist'),
    url(r'^nptag/$', 'natourpress.views.nptaglist'),
    url(r'^newnpauthor/$', 'natourpress.views.newnpauthor'),
    url(r'^deletenpauthor/$', 'natourpress.views.deletenpauthor'),
    url(r'^newnptag/$', 'natourpress.views.newnptag'),
    url(r'^setnpauthor/$', 'natourpress.views.setnpauthor'),
    url(r'^setnptag/$', 'natourpress.views.setnptag'),
    url(r'^setkarma/$', 'natourpress.views.setkarma'),
    url(r'^layouts/$', 'natourpress.views.layouts'),
    url(r'^pagemapper/$', 'natourpress.views.pageMapper'),
   # url(r'^login', 'natourpress.views.my_login'),
    (r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'natourpress/login.html'}),
    (r'^logout/$', 'natourpress.views.logout_view'),
    (r'^posts/$', 'natourpress.views.postlist'),
    (r'^post_detail/(?P<post_id>\d+)/$', 'natourpress.views.postDetail'),
    (r'^main/$', 'natourpress.views.main'),
    (r'^test/$', 'natourpress.views.test'),
    (r'^open_karma/(?P<post_id>\d+)/$', 'natourpress.views.openKarma'),
    url(r'^feed/$', 'natourpress.views.fetchfeed'),
)
