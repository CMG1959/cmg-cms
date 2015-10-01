from django.db import models

# Create your models here.

class errorLog(models.Model):
    shiftID = models.IntegerField(verbose_name="Shift")
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    machNo = models.CharField(verbose_name="Machine Number", max_length=10)
    partDesc = models.CharField(verbose_name="Part Description", max_length=50)
    jobID = models.CharField(verbose_name="Job ID", max_length=10)
    inspectionName = models.CharField(verbose_name = 'Inspection Name', max_length=75)
    errorDescription = models.CharField(verbose_name="Error Description", max_length=250)