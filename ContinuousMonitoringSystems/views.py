from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required
import json

class Account:
    def Auth(request):
        groupId = ''
        groups = request.user.groups.all()
        if groups.count() == 1: groupId = groups[0].id
        
        if request.method == 'GET': Account.UserLoginUnique(request.session.session_key)
        if request.method is 'DELETE': logout(request)
        
        if request.method != 'POST': return JsonResponse({'username': request.user.username, 'groups': groupId}, safe=False)
        
        data = json.loads(request.body)
        user = authenticate(request, username=data['username'], password=data['password'])

        if user is None or not user.is_active: return JsonResponse({'username': ''}, safe=False)
        login(request, user)

        return JsonResponse({'username': request.user.username}, safe=False)

    def UserLoginUnique(key):
        try:
            s = Session.objects.get(pk=key)
            Session.objects.filter(~Q(session_key=key), session_data=s.session_data).delete()
        except: pass
        return

    def User(request, id=None):
        if request.method == 'GET': return JsonResponse(Account.GET(request, id), safe=False)
        elif request.method == 'POST': return JsonResponse(Account.POST(request), safe=False)
        elif request.method == 'PUT': return JsonResponse(Account.PUT(request), safe=False)
        elif request.method == 'DELETE': return JsonResponse(Account.DELETE(request, id), safe=False)

    @permission_required('auth.view_user')
    def GET(request, id=None):
        if not request.user.is_superuser : return list(User.objects.filter(groups__gte=request.user.groups.all()[0].id).values('id', 'username', 'email', 'groups'))
        if id == None : return list(User.objects.all().values())
        return model_to_dict(User.objects.get(pk=id), exclude=['groups','password'])
        
    @permission_required('auth.add_user')
    def POST(request):
        data = json.loads(request.body)
        if data['groups'] == None: return {'error': 'no group'}
        if User.objects.filter(username=data['username']).exists(): return {'error': 'exist username'}

        u = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        u.groups.set([Group.objects.get(pk=data['groups'])])
        u.save()

        user_dict = model_to_dict(u, fields=['id', 'username', 'email', 'groups'])
        user_dict['groups'] = user_dict['groups'][0].id
        return user_dict
    @permission_required('auth.change_user')
    def PUT(request):
        data = json.loads(request.body)
        u = User.objects.get(pk=data['id'])
        u.username = data['username']
        u.email = data['email']
        u.groups.set([Group.objects.get(pk=data['groups'])])
        u.save()
        user_dict = model_to_dict(u, fields=['id', 'username', 'email', 'groups'])
        user_dict['groups'] = user_dict['groups'][0].id
        return user_dict
    @permission_required('auth.delete_user')
    def DELETE(request, id):
        u = User.objects.get(pk=id)
        u.delete()
        return model_to_dict(u, fields=['id', 'username', 'email'])

    

    
