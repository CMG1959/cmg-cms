from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class errorLog(models.Model):
    shiftID = models.IntegerField(verbose_name="Shift")
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    machNo = models.CharField(verbose_name="Machine Number", max_length=10)
    partDesc = models.CharField(verbose_name="Part Description", max_length=50)
    jobID = models.CharField(verbose_name="Job ID", max_length=10)
    inspectionName = models.CharField(verbose_name = 'Inspection Name', max_length=75)
    errorDescription = models.CharField(verbose_name="Error Description", max_length=250)

class errorLogTime(models.Model):
    number_of_days = models.IntegerField(verbose_name="Number of days to show errors:",
                                         default=1,
                                         validators=[MinValueValidator(1)])
    def __unicode__(self):
        return '%s' % self.number_of_days

class ProductionSummary(models.Model):
    class Meta:
        verbose_name = 'Production Summary'
        verbose_name_plural = 'Production Summary'
        db_table = 'vInspectionSummary'

    inspection_type = models.CharField(verbose_name='Inspection Type', max_length=9)
    date_created = models.DateTimeField(verbose_name='Date Created')
    job_number = models.CharField(verbose_name='Job Number', max_length=15)
    item_number = models.CharField(verbose_name='Item Number', max_length=15)
    item_description = models.CharField(verbose_name= 'Description', max_length=15)
    test_name = models.CharField(verbose_name= 'Test', max_length=15)
    emp_l_name = models.CharField(verbose_name= 'Last Name', max_length=15)
    emp_f_name = models.CharField(verbose_name= 'First Name', max_length=15)
    inspection_result = models.CharField(verbose_name= 'Inspection Result', max_length=15)
    shift = models.IntegerField()
    report_text = models.CharField(max_length=75, verbose_name='Report Text')