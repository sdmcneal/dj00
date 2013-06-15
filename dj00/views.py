from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello.  You've made it to the dj00.")