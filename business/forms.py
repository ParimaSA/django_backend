from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from nanoid import generate
from .models import Queue, Entry


class QueueForm(ModelForm):
    class Meta:
        model = Queue
        fields = ["name", "alphabet"]
