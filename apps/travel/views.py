from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from . models import *
import bcrypt


# LogIn and Registration:

def index(request):
    return render(request, "travel/welcome.html")

def logInReg(request):
    return render(request, "travel/logInReg.html")

def login(request):
    getForm = request.POST
    hashed_pw = bcrypt.hashpw(getForm['password'].encode(), bcrypt.gensalt())
    user = User.objects.filter(email=getForm['email']) 
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(getForm['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/myTrips')
        else:
            messages.error(request, "Invalid password or email")
            return redirect('/')
    else:
        messages.error(request, "Invalid password or email")
        return redirect('/')

def register(request):
    form = request.POST
    hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
    errors = User.objects.basic_validator(form)
    if len(errors):
        for key, error in errors.items():
            messages.error(request, error, extra_tags=key)
        return redirect("/logInReg")
    else: 
        user = User.objects.create(
        first_name= form['first_name'],
        last_name = form['last_name'],
        email = form['email'],
        password = hashed_pw,
        )
        request.session['user_id'] = user.id
        user = request.session['user_id']
        return redirect("/myTrips", {"user": user})


def myTrips(request):
    user = User.objects.get(id=request.session['user_id'])
    if 'user_id' not in request.session:
        errorMessage = "Please Log-In or Register"
        return render(request, "travel/logInReg.html",  {"logoutMessage":errorMessage})
    else:
        userTravels = user.my_travels.all()
        getAllTravels = Travel.objects.all()
        print("getAllTravels", getAllTravels)
        joinedTravels = user.joined_travels.all()
        print("joinedTravels", joinedTravels)
        return render(request, "travel/userPage.html", {"user":user, "allTravels": getAllTravels, "travelsJoined": joinedTravels})


def create_travels(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        errors = Travel.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error, extra_tags=key)
            return redirect("/createTravelsLink")
        else:
            getTravelInfo = request.POST
            crtTravel = Travel.objects.create(title=getTravelInfo['title'], description=getTravelInfo['description'], location=getTravelInfo['location'], job_planner=User.objects.get(id=request.session["user_id"]))
            user.my_travels.add(crtTravel)
            crtTravel.save()
            return redirect("/myTrips")

    if request.method == 'GET':
        return redirect("/createTravelsLink")


def link(request):
    user = User.objects.get(id=request.session['user_id'])
    return render(request, "travel/create.html", {"user":user})


def travel(request, travel_id):
    travelId= Travel.objects.get(id=travel_id)
    user = User.objects.get(id=request.session['user_id'])
    joinedTravels = user.joined_Travel.all()
    return  render(request, "travel/showItem.html", {"TravelId":travelId, "user":user, "joinedTravels":joinedTravels} )

def editTravels(request, travel_id):
    makeChange = Travel.objects.get(id = travel_id)
    user = User.objects.get(id=request.session['user_id'])
    return render(request, "travel/update.html", {"updateID": makeChange,  "user":user})

def update_travels(request, travel_id):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        errors = Travel.objects.basic_validator(request.POST)
        if len(errors ) > 0:
            for key, error in errors.items():
                messages.error(request, error)
            return redirect("/editTravel/"+travel_id+"/edit")  
        else:
            changeTravel = Travel.objects.get(id=int(request.POST['hidden_trip_id']))
            changeTravel.title = request.POST['title']
            changeTravel.description = request.POST['description']
            changeTravel.location = request.POST['location']
            changeTravel.save()
            return redirect("/myTrips")    

    if request.method == 'GET':
        return redirect("/editTravel/"+travel_id+"/edit")

def joinTravels(request, travel_id):
    thisUser = User.objects.get(id=request.session['user_id'])
    thisTravel = Travel.objects.get(id = travel_id)
    thisUser.joined_travel.add(thisTravel)
    return redirect('/myTrips')

def cancelTravels(request, travel_id):
    thisUser = User.objects.get(id=request.session['user_id'])
    thisJob = Travel.objects.get(id = travel_id)
    thisUser.joined_travels.remove(thisTravel)
    return redirect("/myTrips")


def deleteTravels(request, travel_id):
    dT = Travel.objects.get(id=travel_id)
    dT.delete()
    return redirect("/myTrips")


def logOut(request):
    request.session.clear()
    return redirect('/')   