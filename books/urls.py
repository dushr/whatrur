from django.conf.urls.defaults import *
from django.views.generic import ListView
from books.models import Book

# urlpatterns = patterns('',   
# #     url(r'^$', 'creative.views.questions', name='questions'),
# #     url(r'^task/(?P<action>[delete|done]+)/(?P<task_id>\d+)', 'creative.views.update_task'),
# #     url(r'^task/(?P<task_id>\d+)/$', 'creative.views.task_details', name='show_details'),
# #     url(r'^all/$', 'creative.views.list_all_tasks', name='show_all_tasks'),
# #     url(r'^stats/$', 'creative.views.stats', name='show_stats'),
# # )
urlpatterns = patterns('',
    url(r'^(?P<book_id>\d+)/reads/incr/$', 'books.views.incr_reads', name='incr_reads'),
    url(r'^$', ListView.as_view(
            model=Book
        )),
    )