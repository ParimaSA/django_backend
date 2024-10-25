"""Provide model using in customer app."""

from django.conf import settings
from django.db import models
from business.models import Entry

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CustomerQueue(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
