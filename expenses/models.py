from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Expense(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - ${self.amount}"


class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    completed = models.BooleanField(default=False)
    amount = models.IntegerField(
        default=0, null=True, blank=True)

    STATUS_CHOICES = (
        ('complete', 'Complete'),
        ('inprogress', 'In Progress'),
        ('scheduled', 'Scheduled'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='inprogress'
    )
    scheduled_day = models.DateField(blank=True, null=True)
    priority = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
