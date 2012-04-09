import urllib2
from BeautifulSoup import BeautifulSoup as Soup
from django.conf import settings
from models import Book, Author
'''
This me playing around, tyring to fill in the database.
I am getting best sellers from wikipedia and storing them.
'''

LANGUAGES = ('english','spanish','german','portuguese','italian')

def get_books():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    content = opener.open('http://en.wikipedia.org/wiki/List_of_best-selling_books').read()

    s = Soup(content)

    tables = s.findAll('table')
    books = []
    for table in tables[1:7]:
        rows = table.findAll('tr')
        header = rows[0]
        index_of_original_lang = [h.getText().lower() for h in header.findAll('th')].index('original language')
        for d in rows[1:]:
            data = d.findAll('td')
            if [dd.getText().lower() for dd in data][index_of_original_lang] in LANGUAGES:
                a = data[0].find('a')
                author = data[1]
                _dict = {
                    'link': a.get('href'),
                    'title': a.get('title'),
                    'author': author.getText(),
                }
                books.append(_dict)

    return books

def update_books(books = get_books()):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    for book in books:
        try:
            b = Book.objects.filter(title=book['title']).count()
            print '>>>', b
            if not b:
                b = Book()
                b.title = book['title']
                author = book['author']
                last_name = author.split(' ')[-1]
                first_name = ' '.join(author.split(' ')[:-1])
                try:
                    author = Author.objects.get(first_name=first_name, last_name=last_name)
                except:
                    author = Author(first_name=first_name, last_name=last_name)
                    author.save()
                b.author = author
                b.external_url = 'http://en.wikipedia.org'+book['link']
                try:
                    content = opener.open('http://en.wikipedia.org'+book['link']).read()
                    s = Soup(content)
                    info = s.find('table', {'class':'infobox'})
                    img = info.find('img')
                    if img:
                        b.image = 'http:'+img.get('src')
                except:
                    print "IMAGE FAILED FOR", book
                b.save()
        except Exception, e:
            print e
            print "WOAH TOTAL FAILURE", book

def get_books_ml():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    content = opener.open('http://www.modernlibrary.com/top-100/100-best-novels/').read()

    s = Soup(content)
    books = []
    _list = []
    for bl in s.findAll('div', {'class':'list-100'}):
        _list += bl.findAll('li')

    for b in _list:
        title = b.find('strong').getText().title()
        author = b.getText()[b.getText().find('by')+3:]
        books.append({
            'title':title,
            'author':author,
            })

    for book in books:
        try:
            b = Book.objects.filter(title=book['title']).count()
            print '>>>', b
            if not b:
                b = Book()
                b.title = book['title']
                author = book['author']
                last_name = author.split(' ')[-1]
                first_name = ' '.join(author.split(' ')[:-1])
                try:
                    author = Author.objects.get(first_name=first_name, last_name=last_name)
                except:
                    author = Author(first_name=first_name, last_name=last_name)
                    author.save()
                b.author = author
                b.save()
        except Exception, e:
            print e
            print "WOAH TOTAL FAILURE", book
