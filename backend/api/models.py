from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Organizer(models.Model):
    """
    An Organizer model class contains organizer attributes
    and a method...
    """
    organizer_name = models.CharField(max_length=100)
    email = models.EmailField()
    event_list = models.ManyToManyField(Event, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.user.first_name
    