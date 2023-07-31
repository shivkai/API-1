from django.db import models
# Create your models here.

class Pokemondata(models.Model):
    name = models.CharField(max_length=200)
    attribute = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    height = models.CharField(max_length=200)
    evolution = models.CharField(max_length=200)

    def __str__(self):
        return self.name
