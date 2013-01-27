from django.conf.urls.defaults import patterns


urlpatterns = patterns('djblets.exthandler.views',
                       (r'^$', 'add_extension'),
                       )
