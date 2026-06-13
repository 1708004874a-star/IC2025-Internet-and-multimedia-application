from django.db import models

# Create your models here.
class sensor(models.Model):
    node_id = models.CharField(max_length=10)  
    loc = models.CharField(max_length=50)    
    temp = models.DecimalField(max_digits=5, decimal_places=2)  
    hum = models.DecimalField(max_digits=5, decimal_places=2)   
    light = models.DecimalField(max_digits=5, decimal_places=2)  
    snd = models.DecimalField(max_digits=5, decimal_places=2)   
    date_created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = 'sensors'

    def __str__(self):
        return 'sensor #{}'.format(self.id)