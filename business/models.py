"""Provide model using in business app."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from nanoid import generate
from django.forms import ModelForm


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Queue(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    alphabet = models.CharField(max_length=1, default='A')
    estimated_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    name = models.CharField(max_length=50)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    tracking_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    time_in = models.DateTimeField(default=timezone.now)
    time_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='waiting')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.tracking_code and self.status != 'completed':
            while True:
                new_tracking_code = generate('1234567890abcdefghijklmnopqrstuvwxyz', size=10)
                if not Entry.objects.filter(tracking_code=new_tracking_code, time_out__isnull=True).exists():
                    self.tracking_code = new_tracking_code
                    break

        if not self.name:
            today = timezone.now().date()
            queue_entries_today = Entry.objects.filter(queue=self.queue, time_in__date=today).count() + 1
            self.name = f"{self.queue.alphabet}{queue_entries_today}"

        super().save(*args, **kwargs)

    def mark_as_completed(self):
        self.status = 'completed'
        self.time_out = timezone.now()
        self.tracking_code = None
        self.save()

    def is_waiting(self):
        return self.status == 'waiting'
