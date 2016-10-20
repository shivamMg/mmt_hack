from django.db import models


class Continent(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.code


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent)

    def __str__(self):
        return self.code
