from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message', 'created_at']
    