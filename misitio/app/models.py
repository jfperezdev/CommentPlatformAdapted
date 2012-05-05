from django.db import models

class Coche(models.Model):
gasolina = models.CharField(maxlength=30)

