from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.conf import settings

from models import Exercise

def oembed(request):
  if 'url' not in request.GET: #nothing to do in this case
    return HttpResponseBadRequest()
  else:
    e = get_object_or_404(Exercise, url=request.GET['url'])
    data = {"version": "1.0", "type": "rich", 
            "html": render_to_string("applet.html", {"e": e}),
            "width": e.width, "height": e.height}
    format = request.GET.get('format', 'json')
    if format == 'json':
      return _jsonresponse(request, data)
    elif format == 'xml':
      return _xmlresponse(request, data)
    else:
      # if not a known format, return HTTP Error 501 Not implemented
      return HttpResponse("Unknown format: %s"%format, status=501)
    
def _jsonresponse(request, data):
  respjson = json.dumps(data)
  if 'callback' in request.GET:
    respjson = '%s(%s);'%(request.GET['callback'], respjson)
  return HttpResponse(respjson, mimetype="text/plain")
  
def _xmlresponse(request, data):
  from django.template.defaultfilters import escape
  return HttpResponse(render_to_string("resp.xml", {"data":data}), mimetype="text/plain")