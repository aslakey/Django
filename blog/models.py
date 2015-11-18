from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title