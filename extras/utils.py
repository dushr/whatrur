from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import urllib2


def upload_to_s3(content, filename, bucket=settings.DEFAULT_BUCKET, content_type=None):
    conn = S3Connection(settings.AWS_ID,settings.AWS_KEY)
    try:
        b = conn.get_bucket(bucket)
    except:
        b = conn.create_bucket(bucket)
        b.set_acl('public-read')
    k = Key(b)

    k.key = filename
    if content_type:
        k.set_metadata("Content-Type", content_type)
    k.set_contents_from_string(content)
    k.set_acl('public-read')
    url = filename
    return url

def get_image_content(url):
        try:
            image = urllib2.urlopen(url.strip().replace(' ','%20'))
            imgContentType = image.info().getheader('Content-Type')
            if imgContentType not in ('image/png','image/bmp','image/jpeg', 'image/pjpeg', 'image/x-png'):
                checkContentType = False
            else:
                checkContentType = True
        except Exception, e:
            ## Log it here
            return None
        _file = ''
        _success_read = False
        if checkContentType:
            while 1:
                try:
                    data = image.read(8192)
                    if not data:
                        break
                    _file += data
                except Exception, e:
                    break
                else:
                    _success_read = True
        if _success_read:
            return {'data':_file, 'Content-Type':imgContentType}
        return None