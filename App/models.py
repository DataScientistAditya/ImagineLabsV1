from django.db import models

# Create your models here.


class PptData(models.Model):
    Query = models.CharField(max_length=500)
    isLayman = models.BooleanField(default=True)
    FileLoc = models.FileField(upload_to="PptFiles",default="N/a")
    
    