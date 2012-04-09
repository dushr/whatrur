from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from books.models import Book

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whatrur.views.home', name='home'),
    # url(r'^whatrur/', include('whatrur.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^books/', include('books.urls')),
    # url(r'^search/', include('books.urls')),
    url(r'^$', 'books.views.index'),
)
