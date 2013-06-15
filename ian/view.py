# from statements tell python that you're going to use libraries of pre-built functions/code
from django.http import HttpResponse
from django.shortcuts import render

# This is what a comment looks like.  It starts with a pound sign '#'

def firstresponse(request):
    return HttpResponse('Hello World')


def firstpage(request):
    context = { 'hello_message': 'Hi There!',}
    return render(request,'ian/iansfirstwebpage.html',context)


