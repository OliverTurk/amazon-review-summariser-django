from django.db import models

class Summary(models.Model):
    summary = models.CharField(max_length=255)
class URL(models.Model):
    url = models.CharField