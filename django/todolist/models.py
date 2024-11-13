from django.db import models
from datetime import datetime

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=350)
    description=models.CharField(max_length=350)
    complete=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.title, self.description
    
    def formatted_date(self):
        return self.created_at.strftime('%d-%m-%Y %H:%M')
