from django.db import models

# Create your models here.
class Item(models.Model):
    item_no = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    desription = models.CharField(max_length=300)
    brand = models.CharField(max_length=100)
    unit_price = models.IntegerField()
    stock = models.IntegerField()
    created_date = models.DateTimeField()

    def __str__(self):
        return 'Item #{}'.format(self.id)

    class Meta:
        verbose_name_plural = 'Items'