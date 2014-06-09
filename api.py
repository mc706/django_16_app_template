from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from .models import Object
from .forms import ObjectForm

@login_required
def list_objects(request):
    """
    list all objects for an account
    """
    if request.method == "GET":
        objects = Object.objects.filter(account__id=request.user.id)
        return HttpResponse(status=200,content_type="application/json",content=render(request,'api/objects.json',{'objects':objects}))
    else:
        return HttpResponse(status=405)


@login_required
def object(request, object_slug=None):
    if object_slug and object_slug != "new":
        try:
            object = Object.objects.get(Q(slug=object_slug), Q(account=request.user) | Q(shared__id=request.user.id))
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
    if request.method == "POST" and object_slug == "new":
        try:
            form = ObjectForm(request.POST)
            if form.is_valid():
                object = form.save(commit=False)
                object.account = request.user
                object.save()
                return HttpResponse(status=201,content_type="application/json",content=render(request,"api/object.json",{'object':object}))
            else:
                print form.errors
                return HttpResponse(status=500, content_type="text/plain", content=form.errors)
        except Exception as ex:
            print ex
            return HttpResponse(status=500, content_type="text/plain", content=ex)
    elif request.method == "PUT":
        put = QueryDict(request.body)
        try:
            form = ObjectForm(put, instance=object)
            if form.is_valid():
                updated = form.save(commit=False)
                updated.save()
                return HttpResponse(status=200, content_type="application/json", content=render(request, 'api/object.json', {'object': updated}))
            else:
                print form.errors
                return HttpResponse(status=500, content_type="text/plain", content=form.errors)
        except Exception as ex:
            print ex
            return HttpResponse(status=500, content_type="text/plain", content=ex)
    elif request.method == "DELETE":
        try:
            object.delete()
            return HttpResponse(status=200)
        except Exception as ex:
            print ex
            return HttpResponse(status=500, content_type='text/plain', content=ex)
    elif request.method == "GET":
        return HttpResponse(status=200,content_type="application/json",content=render(request,'api/object.json',{'object':object}))
    else:
        return HttpResponse(status=405)
