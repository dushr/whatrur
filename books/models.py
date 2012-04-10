from django.db import models
from extras.utils import upload_to_s3, get_image_content, generate_url
import hashlib, random
from django.conf import settings
from djangosphinx import SphinxSearch
import urllib,urllib2
import json

# Create your models here.
required = {
    'blank':False,
    'null':False,
}
optional = {
    'blank':True,
    'null':True
}
class Book(models.Model):
    title = models.CharField(max_length=255, **required)
    author = models.ForeignKey('Author', **optional)
    isbn = models.CharField(max_length=50, **optional) ##TODO make sure this is unique.
    readers = models.IntegerField(default=0)
    external_url = models.URLField(**optional)
    rating = models.DecimalField(default='2.5', decimal_places=2, max_digits=3)
    related_books = models.CharField(max_length=150, **optional)
    image = models.CharField(max_length=255, **optional)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if self.image and self.image.startswith('http://'):
        #     self.save_image_to_s3()
        super(Book, self).save(*args, **kwargs)

    def save_image_to_s3(self, call_save=False):
        '''
        - Gets the image content from the url saved in the image field
        - uploads the image to s3 using the helper function
        - rewrites the image field with the new url.
        '''
        image_data = get_image_content(self.image)
        if image_data:
            image = upload_to_s3(image_data['data'], self.get_image_name(generate=True), content_type=image_data['Content-Type'])
            if image:
                self.image = image
        if call_save:
            super(Book, self).save(*args, **kwargs)


    def get_image_name(self, generate=False):
        '''
        returns the image field.
        if generate flag is set, we sha1 the isbn if it exists.
        else we sha1 the title and a random integer.
        '''
        if generate:
            if self.isbn:
                return hashlib.sha1(self.isbn).hexdigest()
            else:
                return hashlib.sha1(self.title + str(random.randint(0,10000))).hexdigest()

        return self.image

    def get_img_url(self):
        if self.image and not self.image.startswith('http://'):
            return generate_url([settings.AWS_URL, settings.DEFAULT_BUCKET, self.image])
        # if not self.image:
        #     return self.get_image_suggestions(first=True)
        print self.image
        return self.image

    def incr_reads(self):
        self.readers += 1
        self.save()
        return self.readers

    def get_image_suggestions(self, first=True):
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s'
        q = urllib.urlencode({'q':self.title + ' cover'})
        r = urllib2.urlopen(url%q)
        r = json.loads(r.read())
        results = r['responseData']['results']
        _img = []
        for r in results:
            _img.append(r['url'])
        
        if first:
            return _img[0]
        return _img


    search = SphinxSearch(index='books')


class Author(models.Model):
    first_name = models.CharField(max_length=100, **optional)
    last_name = models.CharField(max_length=100)
    website = models.URLField(**optional)
    image = models.CharField(max_length=20, **optional)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s' %(self.last_name, self.first_name)


