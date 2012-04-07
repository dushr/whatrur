from django.db import models
from extras.utils import upload_to_s3, get_image_content
import hashlib, random

# Create your models here.
required = {
    'blank':False,
    'null':False,
}
not_required = {
    'blank':True,
    'null':True
}
class Book(models.Model):
    title = models.CharField(max_length=255, **required)
    author = models.ForeignKey('Author', **not_required)
    isbn = models.CharField(max_length=50, **not_required)
    readers = models.IntegerField(default=0)
    external_url = models.URLField(**not_required)
    rating = models.DecimalField(default=2.5, decimal_places=2, max_digits=3)
    related_books = models.CharField(max_length=150, **not_required)
    image = models.CharField(max_length=255, **not_required)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image and self.image.startswith('http://'):
            self.save_image_to_s3()
        super(Book, self).save(*args, **kwargs)

    def save_image_to_s3(self):
        image_data = get_image_content(self.image)
        if image_data:
            image = upload_to_s3(image_data['data'], self.get_image_name(generate=True), content_type=image_data['Content-Type'])
            if image:
                self.image = image

    def get_image_name(self, generate=False):
        if generate:
            return hashlib.sha1(self.title + str(random.randint(0,10000))).hexdigest()

        return self.image


class Author(models.Model):
    first_name = models.CharField(max_length=20, **not_required)
    last_name = models.CharField(max_length=20)
    website = models.URLField(**not_required)
    image = models.CharField(max_length=20, **not_required)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s' %(self.last_name, self.first_name)


