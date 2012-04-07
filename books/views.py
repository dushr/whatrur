# Create your views here.
from django.shortcuts import render_to_response, Http404, render
from django.template import RequestContext
from django.views.generic.base import TemplateView

class NewBookView(TemplateView):
    template_name = 'books/new.html'

    def get(self, request, *args, **kwargs):
        form = NewBookForm()
        context = {
            'form':form,
        }
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        form = NewBookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)