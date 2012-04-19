from django.db import models


class SomeModel(models.Model):
    field = models.CharField(max_length=50)
