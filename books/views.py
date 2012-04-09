# Create your views here.
from django.shortcuts import render_to_response, Http404, render
from django.template import RequestContext
from books.models import Book
from django.http import HttpResponse

def incr_reads(request, book_id):
    if request.POST:
        try:
            readers = Book.objects.get(id=book_id).incr_reads()
            return HttpResponse(readers)
        except Book.DoesNotExist:
            pass
    return HttpResponse('FAILED')

def index(request):
    '''
    No processing, should use direct to template.
    '''
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def search(request):
    if request.GET and 'q' in request.GET:
        b = Book.search.query(request.GET['q'])
    return render_to_response('books/book_list.html', {'object_list':b}, context_instance=RequestContext(request))

