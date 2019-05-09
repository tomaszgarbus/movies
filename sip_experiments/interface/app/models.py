from django.db import models

# Create your models here.


class Document(models.Model):
    """
    A single document - tax interpretation.
    """
    filename = models.CharField(max_length=7)
