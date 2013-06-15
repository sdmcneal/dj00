from django.http import HttpResponse
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django import forms
from django.forms import ModelForm
from django.template import Context, loader
from django.shortcuts import render
from models import Track,Place
import glob
import os
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.staticfiles import storage
import time
import datetime
from datetime import datetime
from math import pow,sqrt

color_lookup = {};
next_color_index = 0

class TrackForm(ModelForm):
    class Meta:
        model = Track
        
class TrackCreate(CreateView):
    model = Track
    
class TrackUpdate(UpdateView):        
    model = Track
    
class TrackDelete(DeleteView):
    model = Track
    
class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['place','user','latitude','longitude']
    
class DistancePair:
    def __init__(self, pairarg, distarg, lat1arg,long1arg,lat2arg,long2arg):
        self.pair = pairarg
        self.distance = distarg
        self.lat1 = lat1arg
        self.long1 = long1arg
        self.lat2 = lat2arg
        self.long2 = long2arg
        
class UserCheckin:
    def __init__(self, userarg, timestring ):
        n = datetime.now()
        td = datetime.strptime(timestring, "%Y%m%d%H%M%S")
        d = n - td
        self.age = "%i days %i seconds" %(d.days,d.seconds)
        self.user = userarg
    def __repr__(self):
        return "%s: %s" % (self.user,self.age)
    

    

# calculates how far each user is away from each place
# send array distances to html page with definition [ location pair discription, distance ]
# sends locations of all places and users in array
def how_far(request):
    # get last known location of users
    track1 = Track.objects.filter(user__exact='228E5B5D-3CF9-4A9E-B1F4-ADED7738FF86')
    point1 = track1.order_by('-id')[:1]
    track2 = Track.objects.filter(user__exact='2B5653E5-AE0F-4B36-B903-E2FBDCD45ADB')
    point2 = track2.order_by('-id')[:1]
    user_locations = [point1[0],point2[0]]
    user_checkins = [ UserCheckin(point1[0].user,point1[0].datetime),UserCheckin(point2[0].user,point2[0].datetime) ]
    print "checkins = ",user_checkins[0],user_checkins[1]
    
    # get all place locations
    places = Place.objects.all()
    distances = []
    
    # calculate all the distances
    for place in places:
        for user in user_locations:
            pair = "Between %s and %s" % (place.place,user.user)
            distance = calc_distance(place.latitude,place.longitude,user.latitude,user.longitude)
            distances.append(DistancePair(pair,distance,place.latitude,place.longitude,user.latitude,user.longitude))
            
    #print "distances=",distances
    #print "distances[0][0]",distances[0][0]
    context = { 'users':user_locations, 'distances':distances,'places':places,'checkins':user_checkins }
    return render(request,'gps/distances.html',context)
    
    
# returns distance in kilometers between two map locations
def calc_distance(lat1,long1,lat2,long2):
    try:
        return sqrt( pow(lat1 - lat2,2) + pow(long1 - long2,2)) * 111.325        
    except:
        return -1

 
color_array= [ "483d8b", "0000cd", "48d1cc", "daa520", "ff4500", "dda0dd", "ff0000"] 
    
def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            print "place=",form.cleaned_data['place']
            print "user=",form.cleaned_data['user']
            print "latitude=",form.cleaned_data['latitude']
            print "longitude=",form.cleaned_data['longitude']
            
            form.save()
            return HttpResponse("Thanks!")
        else:
            raise Http404
    else:
        form = PlaceForm()
        return render(request,'gps/place_form.html', { 'form': form ,})
    

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = TrackForm(request.GET)
        if form.is_valid():
            td = time.strptime(form.cleaned_data['datetime'], "%Y%m%d%H%M%S")
            print "build=3" 
            print "user=",form.cleaned_data['user']
            print "datetime=",td
            print "latitude=",form.cleaned_data['latitude']
            print "longitude=",form.cleaned_data['longitude']
            print "altitude=",form.cleaned_data['altitude']
            print "waypoint=",form.cleaned_data['waypoint']
            
            form.save()
        
            return HttpResponse(form.cleaned_data['datetime'])
        else:
            raise Http404

def entry(request):
    TrackFormSet = modelformset_factory(Track)
    formset = TrackFormSet()
    context = {'formset':formset,}
    return render(request, 'gps/index.html',context)

#@login_required('gps/accounts/login/')
def map(request):
    context = get_map_points(request)
    return render(request,'gps/map.html',context)

def maplast(request):
    context = get_last_map_points(request)
    return render(request,'gps/map.html',context)

def find_phone_distances():
    home_latitude = 47.542034
    home_longitude = -122.010476
    
    track1 = Track.objects.filter(user__exact='228E5B5D-3CF9-4A9E-B1F4-ADED7738FF86')
    point1 = track1.order_by('-id')[:1]
    track2 = Track.objects.filter(user__exact='2B5653E5-AE0F-4B36-B903-E2FBDCD45ADB')
    point2 = track2.order_by('-id')[:1]
    
    
    distance1 = 0.0
    distance2 = 0.0
    
    if point1:
        distance1 = sqrt( pow(point1[0].latitude - home_latitude,2) + pow(point1[0].longitude - home_longitude,2)) * 111.325
    
    if point2:
        distance2 = sqrt( pow(point2[0].latitude - home_latitude,2) + pow(point2[0].longitude - home_longitude,2)) * 111.325
        
    print "distance1=",distance1
    print "distance2=",distance2

    return

# get_last_map_points()
# is a pilot function to retrieve just the last recorded position of two target phones
# which use hard-coded values
    
def get_last_map_points(request):
    global color_lookup, next_color_index
    
    track1 = Track.objects.filter(user__exact='228E5B5D-3CF9-4A9E-B1F4-ADED7738FF86')
    point1 = track1.order_by('-id')[:1]
    track2 = Track.objects.filter(user__exact='2B5653E5-AE0F-4B36-B903-E2FBDCD45ADB')
    point2 = track2.order_by('-id')[:1]
    
    tracks = [track1[0],track2[0]]

    color_lookup = {}
    d = []
    next_color_index = 0

    color_assignment = [ get_color(t.user) for t in tracks ]
    for t in tracks:
        color_assignment = get_color(t.user)
        d.append( {'id':t.id,'latitude': t.latitude, 'longitude':t.longitude, 'color':color_assignment})

    
    context = {'tracks':d,'colors':color_assignment,'color_lookup':color_lookup}
    return context
        
def get_map_points(request):
    global color_lookup, next_color_index
    
    # temporary
    find_phone_distances()
        
    start = time.time()
    #if request.user.is_authenticated():
    color_lookup = {}
    
    d = []
    next_color_index = 0
    tracks = Track.objects.order_by('-id')[:35]
    color_assignment = [ get_color(t.user) for t in tracks ]
    for t in tracks:
        color_assignment = get_color(t.user)
        d.append( {'id':t.id,'latitude': t.latitude, 'longitude':t.longitude, 'color':color_assignment})
    
#    print "d=",d
#    print "color_lookup=",color_lookup
    elapsed = time.time()-start
    
    message = "Passing the good word from python"
    context = {'message':message,'tracks':d,'colors':color_assignment,'color_lookup':color_lookup,'elapsed':elapsed}
    return context
    #else:
    #    return HttpResponse('Login required to use this feature')
def get_color(username):
    global next_color_index,color_array
    
    return_color = "FFFFFF"
    
    if len(color_lookup)>0:
        existing_color = color_lookup.get(username,'none')
        if existing_color == 'none':
            return_color = color_array[next_color_index]
            next_color_index = next_color_index + 1
            color_lookup[username] = return_color
        else:
            return_color = existing_color
    else:
        next_color_index = next_color_index + 1
        return_color = color_array[0]
        color_lookup[username]=return_color
        
    return return_color

def console(request):
    if request.user.is_athenticated():
        pass
    else:
        return redirect_to_login('/login/?next=%s' % request.path)
    
def cc(request):
    message = "Passing the good word from python"
    sr = settings.STATIC_ROOT+'gps/'
    
    os.chdir(sr)
    
    files = filter(os.path.isfile, os.listdir(sr))
#    filespath = [os.path.join('gps'/,f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    files = [ 'gps/' + f for f in files]
    print "file=", files
    context = {'thepath':sr,'images':files}
    
    return render(request,'gps/cc.html',context)
#def login(request):

def bingmap(request):
    context=get_map_points(request)
    return render(request,'gps/bingmaps.html',context)
    