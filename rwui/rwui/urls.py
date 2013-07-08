from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import wordui.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#url(r'^$', wordui.views.ListPrefixView.as_view(),
#        name = 'prefixes-list'),

urlpatterns = patterns('',
    url(r'^$', wordui.views.noforms, name='index.html'),
    url(r'^index.html$', wordui.views.noforms, name='index.html'),
    url(r'^newwords.html$', wordui.views.inflectedformslower, name = 'newwords.html'),
    url(r'^propernames.html$', wordui.views.inflectedformsupper, name = 'propernames.html'),
    url('wid/(\d+)/', wordui.views.edit_word, name='word_detail.html')
)

urlpatterns += staticfiles_urlpatterns()
