from django.http import JsonResponse
from django.contrib.auth import authenticate, login


from .models import System, Source, Original, Correction, Avg5Minute, Avg1Hour, Avg1Date, Avg1Month
import json
# Create your views here.

def Test(request) : 
    if request.method == 'POST':
        print(json.loads(request.body))

    return JsonResponse({'response': request.method}, safe=False)

def Task(request, run) :

    if run == 'All' :
        return
    elif run == '':
        return
    return JsonResponse({'response': run}, safe=False)

def RESTful_System(request, id=None):
    if request.method == 'GET': return JsonResponse(System.GET(request, id), safe=False)
    elif request.method == 'POST': return JsonResponse(System.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(System.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(System.DELETE(request, id), safe=False)

def RESTful_Source(request, id=None):
    if request.method == 'GET': return JsonResponse(Source.GET(request, id), safe=False)
    elif request.method == 'POST': return JsonResponse(Source.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Source.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Source.DELETE(request, id), safe=False)

def RESTful_Original(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Original.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Original.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Original.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Original.DELETE(request, id), safe=False)

def RESTful_Correction(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Correction.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Correction.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Correction.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Correction.DELETE(request, id), safe=False)

def RESTful_Avg5Minute(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Avg5Minute.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Avg5Minute.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Avg5Minute.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Avg5Minute.DELETE(request, id), safe=False)

def RESTful_Avg1Hour(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Avg1Hour.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Avg1Hour.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Avg1Hour.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Avg1Hour.DELETE(request, id), safe=False)

def RESTful_Avg1Date(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Avg1Date.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Avg1Date.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Avg1Date.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Avg1Date.DELETE(request, id), safe=False)

def RESTful_Avg1Month(request, date=None, count=1, id=None):
    if request.method == 'GET': return JsonResponse(Avg1Month.GET(request, date, count), safe=False)
    elif request.method == 'POST': return JsonResponse(Avg1Month.POST(request), safe=False)
    elif request.method == 'PUT': return JsonResponse(Avg1Month.PUT(request), safe=False)
    elif request.method == 'DELETE': return JsonResponse(Avg1Month.DELETE(request, id), safe=False)
