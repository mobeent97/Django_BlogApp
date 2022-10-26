from multiprocessing import context
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import is_valid_path
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    ).order_by('-created')[0:3]
    # home_messages = Message.objects.all().order_by('-created')
    topics= Topic.objects.all()[0:5]
    context = {
        'rooms':rooms,
        'topics':topics,
         'room_count':room_count,
          'room_messages':room_messages
          }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room= Room.objects.get(id=pk)
    # LOADING ALL MESSAGES
    room_messages = room.message_set.all().order_by('-created')
    participants=room.participants.all()
    # POSTING A NEW MESSAGE
    if request.method == 'POST':
        message = Message.objects.create(user = request.user, room = room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('RoomPage', pk=room.id) 
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='LoginPage')
def createRoom(request):
    form = RoomForm()   
    topics = Topic.objects.all() 
    # Processing/Saving of the Form
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(host = request.user, topic = topic, name = request.POST.get('name'), description = request.POST.get('description'))
        return redirect('HomePage')
    context={'form':form,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='LoginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)    
    form = RoomForm(instance=room)
    topics=Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!!')
    # Processing/Updating of the Form
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('HomePage')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='LoginPage')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)    
    # Processing/Delete of the Room
    if request.method == 'POST':
        room.delete()
        return redirect('HomePage')
    context={'obj':room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='LoginPage')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)    
    # Processing/Delete of the Message
    if request.user != message.user:
        return HttpResponse("You Are Not The owner of the Message So you cant delete!!!")
    if request.method == 'POST':
        message.delete()    
        return redirect('HomePage')
    context={'obj':message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='LoginPage')
def userProfile(request, pk):
    # Get the Requested User from database
    user = User.objects.get(id=pk)        
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('HomepPage')
    # CHECKING IF USER IS AUTHENTICATD
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not Exist')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, 'Username or Password does not exists!!!')
    context={'page':page}
    return render(request, 'base/login_register.html', context)

def registerpage(request):
    form = UserCreationForm(request.POST)
    # REGISTERING A USER
    if request.method =='POST':
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request, 'Registration Successfull!!!')
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, 'An error occurred during registration!!!')
    context={'form':form}
    return render(request, 'base/login_register.html', context)

def logoutpage(request):
    logout(request)
    return redirect('HomePage')

@login_required(login_url='LoginPage')
def updateuser(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method =='POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            redirect('UserProfile',pk=user.id)
    # context={'form':form}
    return render(request, 'base/updateuser.html', {'form':form})

# @login_required(login_url='LoginPage')
def gettopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})


# @login_required(login_url='LoginPage')
def getactivity(request):
    all_messages = Message.objects.all().order_by('-created')
    return render(request, 'base/activity.html',{'room_messages':all_messages})

# @login_required(login_url='LoginPage')
def getSharjeel(request):
    return render(request, 'base/sharjeelbio.html')
