from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        name_regex = re.compile(r'^[a-zA-Z]+')
        email_regex = re.compile(r'^\w+([.-]?\w+)@\w+([.-]?\w+)(.\w{2,3})+$')
        if len(postData['first_name']) < 4 and not name_regex.match('\w', len(postData['first_name'])):
            errors["first_name"] = "First Name should be at least 4 characters"

        if len(postData['last_name']) < 4 and not name_regex.match('\w', len(postData['last_name'])):
            errors["last_name"] = "Last Name should be at least 4 characters"

        if not email_regex.match(postData["email"]):
            errors["email"] = "Please enter valid email"

        if len(postData["password"]) < 2:
            errors["password"] = "Password should be at least 6 characters long."

        if postData["password"] != postData["confirmPassword"]:
            errors["confrimPassword"] = "Your confirm password doesen't match your password"
    
        newUserEmail = User.objects.filter(email=postData['email'])
        existingEmail = []
        for user in User.objects.all():
            existingEmail.append(user.email)
            if postData['email'] in existingEmail:
                errors["email"] = "User already exist!"
        return errors

        return errors

class TravelManager(models.Manager):
    def basic_validator(self, postData):
        print("in validator:",postData)
        errors = {}
        if len(postData["title"]) <= 0:
            errors["title"] = "Title is required"
        elif len(postData["title"]) < 4:
            errors["title"] = "Title must be atlease 3 character long"

        if len(postData["description"]) <= 0:
            errors["description"] = "Description is required"
        elif len(postData["description"]) < 4:
            errors["description"] = "Description must be atlease 3 character long"
      
        if len(postData['location']) <= 0:
            errors["location"] = "Location is required" 
        if len(postData['location']) < 4:
            errors["location"] = "Location must be atlease 3 character long" 
        
        return errors
            

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at =  models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    # my_travels = a list of travels a given user planned
    # joined_travels = list of travels joined by a user
    objects = UserManager()

    def __repr__(self):
        return f"Users: {self.first_name} {self.last_name} {self.id} {self.email} {self.password} {self.my_travels} {self.joined_travels}"


class Travel(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    travel_planner = models.ForeignKey(User, related_name="my_travels")
    # list of users who joined a given travel
    joined_by_users = models.ManyToManyField(User, related_name ="joined_travels")
    objects = TravelManager()

    def __repr__(self):
        return f"Travels: {self.title} {self.id} {self.description} {self.location} {self.travel_planner} {self.joined_by_users}"

