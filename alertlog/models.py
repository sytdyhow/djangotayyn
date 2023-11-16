from django.db import models
from django.contrib.auth.models import User

class Logroles(models.Model):
    name = models.CharField(max_length=150 , null=False)
    description = models.TextField(null=False)
    severity_in = models.CharField(max_length=50, null= False)
    application = models.CharField(max_length = 100, null = False)
    index_number = models.CharField(max_length = 10 ,blank=True,  null=True)
    split_character = models.CharField(max_length =10, null=False)
    start_message = models.CharField(max_length = 10, default =None,blank =True , null=True)
    severity_out = models.CharField(max_length = 10, null =False)
    own_text = models.CharField(max_length = 150 , blank =True, null= True)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name


class Filterlog(models.Model):
    hostname = models.CharField(max_length=150, null=False)
    severity = models.CharField(max_length=50, null=False)
    facility = models.CharField(max_length=50, null=False)
    application = models.CharField(max_length=70, null=False)
    message  = models.TextField(null=False)
    timestamp =models.DateTimeField(auto_now=False)
    role = models.CharField(max_length=350, null=False)
    is_know = models.BooleanField(default =False)
    text_message = models.CharField(max_length=250, default=None, blank=True, null=True)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return (self.hostname + self.message)
    
    
class Hostnames(models.Model):
    hostname  =  models.CharField(max_length=150, null=False)
    ipaddress = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.hostname

class Systems(models.Model):
    name = models.CharField(max_length=100, null=False, blank=True)
    description = models.CharField(max_length=200   , blank=True, null=False)
    url = models.CharField(max_length=100, null = False, blank=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    active = models.BooleanField(default=True)
    icon = models.CharField(max_length=150, null=False, blank=True)
    
    def __str__(self) -> str:
        return  self.name


class Rule(models.Model):
    role_name = models.CharField(max_length=150)

    def __str__(self):
        return self.role_name



    
    
    
class UsersSystem(models.Model):
    users_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    system_id = models.ForeignKey(Systems, on_delete=models.CASCADE, null=True, blank=True)


class UsersRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    role_id = models.ForeignKey(Rule, on_delete=models.CASCADE, null=True,blank=True)



class Userperimision(models.Model):
    name = models.CharField(max_length=150, null=False)
   
class Profile(models.Model):
    title = models.CharField(max_length=100,null=False)
    usersperimission = models.ManyToManyField(Userperimision)
       
    
    def __str__(self) -> str:
        return  self.title
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class Room(models.Model):
    name = models.ForeignKey(User, related_name='mess', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
   
