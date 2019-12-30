from django.db import models
from django.db.models import Count, Max
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required

from django.utils.dateparse import parse_datetime
from datetime import datetime, date, time, timedelta
import json
# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length = 40)
    ph_min = models.FloatField()
    ph_max = models.FloatField()
    ph_offset = models.FloatField()
    ph_unit = models.CharField(max_length = 10, null=True, blank=True)
    ohm_min = models.FloatField()
    ohm_max = models.FloatField()
    ohm_offset = models.FloatField()
    ohm_unit = models.CharField(max_length = 10, null=True, blank=True)
    liter_min = models.FloatField()
    liter_max = models.FloatField()
    liter_offset = models.FloatField()
    liter_unit = models.CharField(max_length = 10, null=True, blank=True)
    celsius_min = models.FloatField()
    celsius_max = models.FloatField()
    celsius_offset = models.FloatField()
    celsius_unit = models.CharField(max_length = 10, null=True, blank=True)
    @permission_required('water.view_source')
    def GET(request, id):
        if id == None: return list(Source.objects.all().values())
        return model_to_dict(Source.objects.get(pk=id))
    @permission_required('water.add_source')
    def POST(request):
        data = json.loads(request.body)
        s = Source.objects.filter(name=data['name']).first()
        if s != None: return model_to_dict(s)
        s = Source()
        s.name = data['name']
        s.save()
        return model_to_dict(s)
    @permission_required('water.change_source')
    def PUT(request):
        data = json.loads(request.body)
        s = Source.objects.get(pk=data['id'])
        s.name = data['name']
        s.save()
        return model_to_dict(s)
    @permission_required('water.delete_source')
    def DELETE(request, id):
        s = Source.objects.get(pk=id)
        s.delete()
        return model_to_dict(s)

class Original(models.Model):
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    upload = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add = False)
    camera = models.CharField(max_length = 4)
    ph = models.FloatField()
    ohm = models.FloatField()
    liter = models.FloatField()
    celsius = models.FloatField()
    class Meta:
        unique_together = ['source', 'timestamp']
    @permission_required('water.view_original')
    def GET(request, id):
        if id == None: return list(Original.objects.all().values())
        return model_to_dict(Original.objects.get(pk=id))
    @permission_required('water.add_original')
    def POST(request):
        data = json.loads(request.body)
        o = Original()
        o.source = Source.objects.get(pk=data['source'])
        o.timestamp = data['timestamp']
        o.camera = data['camera']
        o.ph = data['ph']
        o.ohm = data['ohm']
        o.liter = data['liter']
        o.celsius = data['celsius']
        o.save()

        c = Correction(original=o)
        c.ph = o.ph
        c.ph_s = data['ph_s']
        c.ohm = o.ohm
        c.ohm_s = data['ohm_s']
        c.liter = o.liter
        c.liter_s = data['liter_s']
        c.celsius = o.celsius
        c.celsius_s = data['celsius_s']
        c.save()
        return model_to_dict(c)
    @permission_required('water.change_original')
    def PUT(request):
        data = json.loads(request.body)
        o = Original.objects.get(pk=data['id'])
        o.source = Source.objects.get(pk=data['source'])
        o.timestamp = data['timestamp']
        o.camera = data['camera']
        o.ph = data['ph']
        o.ohm = data['ohm']
        o.liter = data['liter']
        o.celsius = data['celsius']
        o.save()
        return model_to_dict(o)
    @permission_required('water.delete_original')
    def DELETE(request, id):
        o = Original.objects.get(pk=id)
        o.delete()
        return model_to_dict(o)

class Correction(models.Model):
    original = models.OneToOneField(Original, on_delete=models.CASCADE, primary_key=True )
    ph = models.FloatField()
    ph_s = models.IntegerField()
    ohm = models.FloatField()
    ohm_s = models.IntegerField()
    liter = models.FloatField()
    liter_s = models.IntegerField()
    celsius = models.FloatField()
    celsius_s = models.IntegerField()
    @permission_required('water.view_correction')
    def GET(request, date, count):
        if date == None :
            c = Correction.objects.latest('original__timestamp')
            result = model_to_dict(c)
            result['timestamp'] = c.original.timestamp
            result['source'] = c.original.source
            result['camera'] = c.original.camera
            return result
        start = parse_datetime(date)
        end = start + timedelta(minutes=count-1)
        result = list(Correction.objects.filter(original__timestamp__range=(start,end)).order_by('original__timestamp')
        .values('original__source', 'original__timestamp', 'original__camera', 'ph', 'ph_s', 'ohm', 'ohm_s', 'liter', 'liter_s', 'celsius', 'celsius_s'))
        for c in result: 
            c['timestamp'] = c.pop('original__timestamp')
            c['source'] = c.pop('original__source')
            c['camera'] = c.pop('original__camera')
        return result
    @permission_required('water.add_correction')
    def POST(request):
        data = json.loads(request.body)
        o = Correction()
        o.ph = data['ph']
        o.ph_s = data['ph_s']
        o.ohm = data['ohm']
        o.ohm_s = data['ohm_s']
        o.liter = data['liter']
        o.liter_s = data['liter_s']
        o.celsius = data['celsius']
        o.celsius_s = data['celsius_s']
        o.save()
        return model_to_dict(o)
    @permission_required('water.change_correction')
    def PUT(request):
        data = json.loads(request.body)
        o = Correction.objects.get(pk=data['id'])
        o.ph = data['ph']
        o.ohm = data['ohm']
        o.liter = data['liter']
        o.celsius = data['celsius']
        o.save()
        return model_to_dict(o)
    @permission_required('water.delete_correction')
    def DELETE(request, id):
        o = Correction.objects.get(pk=id)
        o.delete()
        return model_to_dict(o)

class Avg5Minute(models.Model):
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    upload = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add = False)
    camera = models.CharField(max_length = 4)
    ph = models.FloatField()
    ph_s = models.IntegerField()
    ohm = models.FloatField()
    ohm_s = models.IntegerField()
    liter = models.FloatField()
    liter_s = models.IntegerField()
    celsius = models.FloatField()
    celsius_s = models.IntegerField()
    class Meta:
        unique_together = ['source', 'timestamp']
    @permission_required('water.view_avg5minute')
    def GET(request, date, count):
        if date == None :
            result = model_to_dict(Avg5Minute.objects.latest('timestamp'))
            result['source'] = result.pop('source_id')
            return result
        start = parse_datetime(date)
        end = start + timedelta(minutes=5*(count-1))
        result = list(Avg5Minute.objects.filter(timestamp__range=(start,end)).order_by('timestamp').values())
        for c in result:
            c['source'] = c.pop('source_id')
        return result
    @permission_required('water.add_avg5minute')
    def POST(request):
        data = json.loads(request.body)
        a = Avg5Minute()
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.change_avg5minute')
    def PUT(request):
        data = json.loads(request.body)
        a = Avg5Minute.objects.get(pk=data['id'])
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.delete_avg5minute')
    def DELETE(request, id):
        a = Avg5Minute.objects.get(pk=id)
        a.delete()
        return model_to_dict(a)

class Avg1Hour(models.Model):
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    upload = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add = False)
    camera = models.CharField(max_length = 4)
    ph = models.FloatField()
    ph_s = models.IntegerField()
    ohm = models.FloatField()
    ohm_s = models.IntegerField()
    liter = models.FloatField()
    liter_s = models.IntegerField()
    celsius = models.FloatField()
    celsius_s = models.IntegerField()
    class Meta:
        unique_together = ['source', 'timestamp']
    @permission_required('water.view_avg1hour')
    def GET(request, date, count):
        if date == None :
            result = model_to_dict(Avg1Hour.objects.latest('timestamp'))
            result['source'] = result.pop('source_id')
            return result
        start = parse_datetime(date)
        end = start + timedelta(hours=(count-1))
        result = list(Avg1Hour.objects.filter(timestamp__range=(start,end)).order_by('timestamp').values())
        for c in result:
            c['source'] = c.pop('source_id')
        return result
    @permission_required('water.add_avg1hour')
    def POST(request):
        data = json.loads(request.body)
        a = Avg1Hour()
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.change_avg1hour')
    def PUT(request):
        data = json.loads(request.body)
        a = Avg1Hour.objects.get(pk=data['id'])
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.delete_avg1hour')
    def DELETE(request, id):
        a = Avg1Hour.objects.get(pk=id)
        a.delete()
        return model_to_dict(a)

class Avg1Date(models.Model):    
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    upload = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add = False)
    camera = models.CharField(max_length = 4)
    ph = models.FloatField()
    ph_s = models.IntegerField()
    ohm = models.FloatField()
    ohm_s = models.IntegerField()
    liter = models.FloatField()
    liter_s = models.IntegerField()
    celsius = models.FloatField()
    celsius_s = models.IntegerField()
    class Meta:
        unique_together = ['source', 'timestamp']
    @permission_required('water.view_avg1date')
    def GET(request, date, count):
        if date == None :
            result = model_to_dict(Avg1Date.objects.latest('timestamp'))
            result['source'] = result.pop('source_id')
            return result
        start = parse_datetime(date)
        end = start + timedelta(days=(count-1))
        result = list(Avg1Date.objects.filter(timestamp__range=(start,end)).order_by('timestamp').values())
        for c in result:
            c['source'] = c.pop('source_id')
        return result
    @permission_required('water.add_avg1date')
    def POST(request):
        data = json.loads(request.body)
        a = Avg1Date()
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.change_avg1date')
    def PUT(request):
        data = json.loads(request.body)
        a = Avg1Date.objects.get(pk=data['id'])
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.delete_avg1date')
    def DELETE(request, id):
        a = Avg1Date.objects.get(pk=id)
        a.delete()
        return model_to_dict(a)

class Avg1Month(models.Model):    
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    upload = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add = False)
    camera = models.CharField(max_length = 4)
    ph = models.FloatField()
    ph_s = models.IntegerField()
    ohm = models.FloatField()
    ohm_s = models.IntegerField()
    liter = models.FloatField()
    liter_s = models.IntegerField()
    celsius = models.FloatField()
    celsius_s = models.IntegerField()
    class Meta:
        unique_together = ['source', 'timestamp']
    @permission_required('water.view_avg1month')
    def GET(request, date, count):
        if date == None :
            result = model_to_dict(Avg1Month.objects.latest('timestamp'))
            result['source'] = result.pop('source_id')
            return result
        print(date)
        result = list(Avg1Month.objects.filter(timestamp__gte=date).order_by('timestamp')[:count].values())
        for c in result:
            c['source'] = c.pop('source_id')
        return result
    @permission_required('water.add_avg1month')
    def POST(request):
        data = json.loads(request.body)
        a = Avg1Month()
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.change_avg1month')
    def PUT(request):
        data = json.loads(request.body)
        a = Avg1Month.objects.get(pk=data['id'])
        a.source = Source.objects.get(pk=data['source'])
        a.timestamp = data['timestamp']
        a.camera = data['camera']
        a.ph = data['ph']
        a.ph_s = data['ph_s']
        a.ohm = data['ohm']
        a.ohm_s = data['ohm_s']
        a.liter = data['liter']
        a.liter_s = data['liter_s']
        a.celsius = data['celsius']
        a.celsius_s = data['celsius_s']
        a.save()
        return model_to_dict(a)
    @permission_required('water.delete_avg1month')
    def DELETE(request, id):
        a = Avg1Month.objects.get(pk=id)
        a.delete()
        return model_to_dict(a)

class System(models.Model):
    corporation = models.CharField(max_length=40)
    district = models.CharField(max_length=3)
    @permission_required('water.view_system')
    def GET(request, id):
        if id == None: return list(System.objects.all().values())
        return model_to_dict(System.objects.get(pk=id))
    @permission_required('water.add_system')
    def POST(request):
        data = json.loads(request.body)
        s = System()
        s.corporation = data['corporation']
        s.save()
        return model_to_dict(s)
    @permission_required('water.change_system')
    def PUT(request):
        data = json.loads(request.body)
        s = System.objects.get(pk=data['id'])
        s.corporation = data['corporation']
        s.save()
        return model_to_dict(s)
    @permission_required('water.delete_system')
    def DELETE(request, id):
        s = System.objects.get(pk=id)
        s.delete()
        return model_to_dict(s)
