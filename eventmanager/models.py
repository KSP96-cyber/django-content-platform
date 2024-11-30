from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Advent(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    adventmanager_image = models.ImageField(upload_to="eventmanager", null=True, blank=True) #If you want to allow the adventmanager_image field to be optional
    advent_view_count = models.PositiveIntegerField(default=1)
    rsvp_users = models.ManyToManyField(User, related_name='rsvps', blank=True)
    






