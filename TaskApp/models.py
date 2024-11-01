from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    Title = models.CharField(max_length=100, blank=False)
    Description = models.TextField(blank=True)
    Date = models.DateField(blank=False)
    Completed = models.BooleanField(default=False)
  
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)
  
  
    
def __str__(self):
        return self.Title