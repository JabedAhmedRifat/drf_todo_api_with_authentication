from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    priority = models.BooleanField()

    def remaining_time(self):
        return self.deadline - timezone.now()
    
    def __str__(self):
        return self.title