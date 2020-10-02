from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Kouka2(models.Model):
    product = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    delivery = models.CharField(max_length=100)
    price = models.IntegerField(default=0, \
        validators=[MinValueValidator(0),MaxValueValidator(8000)])
    attachment = models.CharField(max_length=100)


    def __str__(self):
        return '<Kouka2:id=' + str(self.id) + ', ' + \
            self.product + '(' + str(self.price) + ')>'
