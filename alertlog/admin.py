from django.contrib import admin
from .models import  *
# Register your models here.


admin.site.register(Hostnames)
admin.site.register(Logroles)
admin.site.register(Filterlog)



admin.site.register(Rule)
admin.site.register(Systems)
admin.site.register(UsersRole)
admin.site.register(UsersSystem)
admin.site.register(Profile)
admin.site.register(Userperimision)

admin.site.register(Room)
