from django.contrib import admin

# Register your models here.
from .models import Queue, Entry, Business

admin.site.register(Queue)
admin.site.register(Entry)
admin.site.register(Business)
