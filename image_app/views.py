from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import FileResponse
from django.contrib import messages
from urllib import parse
from django.utils.encoding import escape_uri_path

from image_app.forms import PostForm
from image_app.models import PostModel
# Create your views here.

def index(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'提交成功！')
            # messages.add_message(request,messages.SUCCESS,'提交成功！')
            return HttpResponseRedirect(reverse('index'))
    else:
        form=PostForm()

    posts=PostModel.objects.all()[:10].only('category','name','created_time')
    context={
        'form':form,
        'posts':posts,
    }
    return render(request,'image_app/index.html',context)


def image_list(request):
    posts=PostModel.objects.all()
    context={'posts':posts}
    return render(request,'image_app/list.html',context)


def download(request,image_path):
    file_path=str(image_path).strip('/')
    file_name=file_path.split('/')[-1]

    file=open(file_path,'rb')
    response=FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response

