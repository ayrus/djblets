from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('djblets.extensionbrowser.views',
    url(r'^$', 'browse_extensions'),
)
