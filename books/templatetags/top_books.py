from django import template
from books.models import Book
import random

register = template.Library()

def top_books(context):
    books = Book.objects.filter(active=True).exclude(image=None).order_by('?')[:7]
    return {
        'books':books,
    }



register.inclusion_tag('templatetags/top_books.html', takes_context=True)(top_books)