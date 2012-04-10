from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from extras.utils import save_email_in_file

class MaintainanceMiddleware:

    def process_request(self, request):
        if not (request.GET and 'pass' in request.GET and request.GET['pass'] == settings.MAINTAINANCE_SECRET):
            if request.POST:
                save_email_in_file(request.POST)
            return render_to_response('maintainance.html',{}, context_instance=RequestContext(request))
