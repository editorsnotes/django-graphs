from django.http import HttpResponse
import json

def json_ld(request, path):
    return HttpResponse(
        json.dumps({"path":path}), content_type="application/json")
