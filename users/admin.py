from django.contrib import admin
from .models import Profile, ContactInfo,Question

# Register your models here.
admin.site.register(Profile)
admin.site.register(ContactInfo)
admin.site.register(Question)