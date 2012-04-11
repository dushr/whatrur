from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from extras.utils import save_email_in_file

class MaintainanceMiddleware:

    def process_request(self, request):
    	BETA_LIST = False
        if not (request.GET and 'pass' in request.GET and request.GET['pass'] == settings.MAINTAINANCE_SECRET):
            if request.POST:
                save_email_in_file(request.POST)
                BETA_LIST = True
            return render_to_response('maintainance.html',{'BETA_LIST':BETA_LIST,}, context_instance=RequestContext(request))
