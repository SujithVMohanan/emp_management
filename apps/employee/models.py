from django.db import models
from apps.users.models import BaseModel

# Create your models here.



class DynamicField(BaseModel):
    label      = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=50, blank=True, null=True)
    order      = models.PositiveIntegerField(default=0)
    section    = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Dynamic Field'
        verbose_name_plural = 'Dynamic Fields'

    def __str__(self):
        return "{}".format(self.label)    
    

class Employee(models.Model):
    dynamic_data = models.JSONField(default=dict, blank=True, null=True )
    
    def __str__(self):
        return f"Employee {self.id}"