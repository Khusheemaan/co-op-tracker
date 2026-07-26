#show Posting in the admin
from django.contrib import admin
from .models import Posting, Application

# Register your models here.
admin.site.register(Posting)
admin.site.register(Application)



